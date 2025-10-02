from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime
# 导入Playwright相关库
from playwright.sync_api import sync_playwright

class ReviewScraper:
    def __init__(self):
        self.reviews = []
        # 确保data目录存在
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        # 本地HTML文件路径（仅用于保存爬取的内容，不用于读取）
        self.html_file = os.path.join(self.data_dir, 'prettified_imdb_reviews.html')
        # Playwright配置
        self.playwright = None
        self.browser = None
        self.page = None
    
    def scrape_reviews_from_html(self):
        """从本地HTML文件中抓取评论数据"""
        if not os.path.exists(self.html_file):
            print(f"错误：文件 {self.html_file} 不存在")
            return []
        
        print(f"从本地文件 {self.html_file} 读取内容...")
        with open(self.html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        reviews = []
        
        # 使用HTML标签结构查找评论元素，减少对具体class的依赖
        review_articles = soup.find_all('article')
        # 过滤出包含评论内容的article元素
        review_articles = [art for art in review_articles if art.find('div', class_=lambda x: x and 'ipc-list-card__content' in x)]
        print(f"找到 {len(review_articles)} 条评论")
        
        for article in review_articles:
            try:
                # 提取评分 - 使用语义化标签和属性，并转换为数值类型
                rating_element = article.find('span', class_=lambda x: x and 'ipc-rating-star--rating' in x)
                rating = None
                if rating_element:
                    try:
                        rating = float(rating_element.text.strip())
                    except ValueError:
                        rating = None
                
                # 提取评论标题 - 使用语义化标签
                title_element = article.find('h3')
                title = title_element.text.strip() if title_element else None
                
                # 提取评论文本 - 使用内容容器标签
                content_element = article.find('div', class_=lambda x: x and 'ipc-html-content-inner-div' in x)
                content = content_element.text.strip() if content_element else None
                
                # 提取用户名
                user_element = article.find('a', {'data-testid': 'author-link'})
                user = user_element.text.strip() if user_element else None
                
                # 提取日期
                date_element = article.find('li', class_='review-date')
                date = date_element.text.strip() if date_element else None
                
                # 提取Helpful计数 - 使用指定选择器并转换为数值类型
                helpful_element = article.find(class_='ipc-voting__label__count--up')
                helpful = 0
                if helpful_element:
                    try:
                        helpful = int(helpful_element.text.strip())
                    except ValueError:
                        helpful = 0
                
                # 提取Not Helpful计数 - 使用指定选择器并转换为数值类型
                not_helpful_element = article.find(class_='ipc-voting__label__count--down')
                not_helpful = 0
                if not_helpful_element:
                    try:
                        not_helpful = int(not_helpful_element.text.strip())
                    except ValueError:
                        not_helpful = 0
                
                # 创建评论字典 - 只保留必要字段
                review = {
                    'review_text': f"{title}\n{content}" if title and content else content or '',
                    'rating': rating,
                    'reply': 'No replies',
                    'Helpful': helpful,
                    'Not Helpful': not_helpful
                }
                
                # 只添加有内容的评论
                if review['review_text']:
                    reviews.append(review)
            
            except Exception as e:
                print(f"处理评论时出错: {e}")
                continue
        
        return reviews
    
    def _init_playwright(self):
        """初始化Playwright浏览器"""
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=True,  # 设置为False可以看到浏览器运行过程
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            )
            self.page = self.browser.new_page()
            # 设置页面超时
            self.page.set_default_timeout(60000)
            print("Playwright浏览器初始化成功")
    
    def _close_playwright(self):
        """关闭Playwright浏览器"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("Playwright浏览器已关闭")
    
    def scrape_imdb_reviews_with_playwright(self, url, target_count=30):
        """使用Playwright动态抓取IMDb评论"""
        try:
            self._init_playwright()
            print(f"使用Playwright访问: {url}")
            
            # 访问目标页面
            self.page.goto(url)
            
            # 等待页面加载完成
            self.page.wait_for_load_state('networkidle')
            
            attempts = 0
            max_attempts = 10
            
            while len(self.reviews) < target_count and attempts < max_attempts:
                # 提取当前页面上的评论
                current_reviews = self._extract_reviews_from_page()
                
                # 添加新评论（去重）
                new_reviews_added = False
                for review in current_reviews:
                    # 通过评论文本去重
                    if review['review_text'] and not any(r['review_text'] == review['review_text'] for r in self.reviews):
                        self.reviews.append(review)
                        new_reviews_added = True
                        print(f"已收集 {len(self.reviews)} 条评论")
                        if len(self.reviews) >= target_count:
                            break
                
                # 如果没有新评论，增加尝试次数
                if not new_reviews_added:
                    attempts += 1
                    print(f"未找到新评论，尝试次数: {attempts}/{max_attempts}")
                else:
                    attempts = 0  # 重置尝试次数
                
                # 只通过点击"加载更多"按钮来加载更多评论，直接使用'.ipc-see-more'选择器
                try:
                    load_more_button = self.page.query_selector('.ipc-see-more')
                    
                    if load_more_button and load_more_button.is_visible():
                        print("点击'25 more'或'加载更多'按钮")
                        load_more_button.click()
                        time.sleep(3)  # 等待加载
                    else:
                        print("未找到'加载更多'按钮")
                        attempts += 1  # 增加尝试次数，避免无限循环
                except Exception as e:
                    print(f"点击'加载更多'按钮时出错: {e}")
                    attempts += 1  # 增加尝试次数，避免无限循环
                
                # 检查是否达到目标数量
                if len(self.reviews) >= target_count:
                    break
            
            # 保存最终的HTML以供参考
            html = self.page.content()
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"HTML内容已保存到 {self.html_file}（仅用于参考，不用于读取）")
            
            # 限制评论数量
            self.reviews = self.reviews[:target_count]
            print(f"成功使用Playwright收集了 {len(self.reviews)} 条评论")
            
        except Exception as e:
            print(f"使用Playwright抓取评论时出错: {e}")
            # 即使出错也尝试提取已加载的评论
            try:
                current_reviews = self._extract_reviews_from_page()
                for review in current_reviews:
                    if review['review_text'] and not any(r['review_text'] == review['review_text'] for r in self.reviews):
                        self.reviews.append(review)
            except:
                pass
        finally:
            # 确保关闭浏览器
            self._close_playwright()
    
    def _extract_reviews_from_page(self):
        """从当前页面提取评论数据"""
        reviews = []
        
        # 获取当前页面的HTML
        html = self.page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # 使用HTML标签结构查找评论元素，减少对具体class的依赖
        review_articles = soup.find_all('article')
        # 过滤出包含评论内容的article元素
        review_articles = [art for art in review_articles if art.find('div', class_=lambda x: x and 'ipc-list-card__content' in x)]
        
        for article in review_articles:
            try:
                # 提取评分 - 使用语义化标签和属性，并转换为数值类型
                rating_element = article.find('span', class_=lambda x: x and 'ipc-rating-star--rating' in x)
                rating = None
                if rating_element:
                    try:
                        rating = float(rating_element.text.strip())
                    except ValueError:
                        rating = None
                
                # 提取评论标题 - 使用语义化标签
                title_element = article.find('h3')
                title = title_element.text.strip() if title_element else None
                
                # 提取评论文本 - 使用内容容器标签
                content_element = article.find('div', class_=lambda x: x and 'ipc-html-content-inner-div' in x)
                content = content_element.text.strip() if content_element else None
                
                # 提取用户名
                user_element = article.find('a', {'data-testid': 'author-link'})
                user = user_element.text.strip() if user_element else None
                
                # 提取日期
                date_element = article.find('li', class_='review-date')
                date = date_element.text.strip() if date_element else None
                
                # 提取Helpful计数 - 使用指定选择器并转换为数值类型
                helpful_element = article.find(class_='ipc-voting__label__count--up')
                helpful = 0
                if helpful_element:
                    try:
                        helpful = int(helpful_element.text.strip())
                    except ValueError:
                        helpful = 0
                
                # 提取Not Helpful计数 - 使用指定选择器并转换为数值类型
                not_helpful_element = article.find(class_='ipc-voting__label__count--down')
                not_helpful = 0
                if not_helpful_element:
                    try:
                        not_helpful = int(not_helpful_element.text.strip())
                    except ValueError:
                        not_helpful = 0
                
                # 创建评论字典 - 只保留必要字段
                review = {
                    'review_text': f"{title}\n{content}" if title and content else content or '',
                    'rating': rating,
                    'reply': 'No replies',
                    'Helpful': helpful,
                    'Not Helpful': not_helpful
                }
                
                # 只添加有内容的评论
                if review['review_text']:
                    reviews.append(review)
            
            except Exception as e:
                print(f"处理单条评论时出错: {e}")
                continue
        
        return reviews
    
    def _generate_sample_reviews(self, count):
        """生成模拟评论数据以确保满足数量要求"""
        print(f"生成 {count} 条模拟评论数据")
        
        sample_texts = [
            "This movie was fantastic! The acting was brilliant and the storyline kept me engaged from start to finish.",
            "I really enjoyed this film. The special effects were amazing and the characters were well developed.",
            "The movie was okay, but I expected more from the plot. Some scenes felt a bit dragged out.",
            "Not my cup of tea. The story was confusing and I couldn't connect with the characters.",
            "Absolutely loved it! Best movie I've seen all year. Will definitely watch it again.",
            "The cinematography was stunning, but the script could have been better. Overall a decent watch.",
            "Great performances by the lead actors, but the supporting cast was underutilized.",
            "This film exceeded my expectations. The directing was masterful and the soundtrack was perfect.",
            "I found the movie to be quite boring. It lacked excitement and the pacing was off.",
            "A must-watch! The plot twists kept me on the edge of my seat throughout the entire film."
        ]
        
        sample_users = ["MovieLover123", "Cinephile456", "FilmBuff789", "Critic101", "Viewer202"]
        
        for i in range(count):
            review = {
                "review_text": sample_texts[i % len(sample_texts)] + " " + 
                             f"This is additional text to make the review longer. " * (i % 3 + 1),
                "rating": (i % 5) + 1,
                "reply": f"Found this review helpful." if i % 3 == 0 else "No replies"
            }
            self.reviews.append(review)
    
    def save_to_json(self, filename='reviews.json'):
        """将收集的评论保存到JSON文件"""
        output_path = os.path.join(self.data_dir, filename)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.reviews, f, ensure_ascii=False, indent=2)
            print(f"成功保存 {len(self.reviews)} 条评论到 {output_path}")
            return output_path
        except Exception as e:
            print(f"保存评论时出错: {e}")
            return None
    
    def collect_reviews(self, max_reviews=30):
        """主函数：收集评论并保存"""
        # 直接使用Playwright从IMDb网站动态抓取，不使用本地HTML文件
        print("直接使用Playwright从IMDb网站抓取评论...")
        imdb_url = 'https://www.imdb.com/title/tt13542714/reviews/?ref_=ttrt_ov_ql_2'
        self.scrape_imdb_reviews_with_playwright(imdb_url, max_reviews)
        
        # 不再使用模拟数据，确保只保存实际抓取的评论
        print(f"最终收集到 {len(self.reviews)} 条真实评论")
        
        # 限制评论数量
        self.reviews = self.reviews[:max_reviews]
        
        # 保存到文件
        self.save_to_json()

# 主程序
if __name__ == "__main__":
    scraper = ReviewScraper()
    scraper.collect_reviews(max_reviews=30)
    
    # 打印前3条评论作为样本
    print("\n前3条评论样本:")
    for i, review in enumerate(scraper.reviews[:3], 1):
        print(f"\n评论 {i}:")
        print(f"评分: {review['rating']}")
        print(f"Helpful: {review['Helpful']}")
        print(f"Not Helpful: {review['Not Helpful']}")
        print(f"文本: {review['review_text'][:100]}...")
        print(f"回复: {review['reply']}")
    
    print(f"\n总共收集到 {len(scraper.reviews)} 条评论")