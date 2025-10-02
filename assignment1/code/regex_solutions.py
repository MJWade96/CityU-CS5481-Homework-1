import re


def test_regex(pattern, test_cases, expected_results):
    """测试正则表达式模式"""
    results = []
    for i, test_case in enumerate(test_cases):
        match = re.fullmatch(pattern, test_case)
        result = bool(match)
        results.append((test_case, result, expected_results[i]))
    return results


def print_test_results(results, description):
    """打印测试结果"""
    print(f"\n{description}")
    print("-" * 80)
    for test_case, result, expected in results:
        status = "✓ 正确" if result == expected else "✗ 错误"
        print(f"测试: '{test_case}' | 结果: {result} | {status}")


def main():
    """主函数：实现并测试所有正则表达式模式"""
    
    # 1. 仅包含字母的字符串
    pattern1 = r'^[a-zA-Z]+$'
    test_cases1 = ['Python', 'DataScience', 'Hello123']
    expected1 = [True, True, False]
    results1 = test_regex(pattern1, test_cases1, expected1)
    print_test_results(results1, "1. 仅包含字母的字符串")
    
    # 2. 以辅音开头的单词
    pattern2 = r'^[b-df-hj-np-tv-zB-DF-HJ-NP-TV-Z]\w*$'
    test_cases2 = ['cat', 'elephant', 'dog', 'owl']
    expected2 = [True, False, True, False]  # 'elephant'和'owl'以元音开头
    results2 = test_regex(pattern2, test_cases2, expected2)
    print_test_results(results2, "2. 以辅音开头的单词")
    
    # 3. 有效的域名
    pattern3 = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    test_cases3 = ['openai.org', 'my-site.net', 'invalid@site']
    expected3 = [True, True, False]
    results3 = test_regex(pattern3, test_cases3, expected3)
    print_test_results(results3, "3. 有效的域名")
    
    # 4. 提取文本中的所有整数
    pattern4 = r'\b\d+\b'
    test_text4 = "He scored 45 goals in 2022 and 10 goals in 2023."
    integers = re.findall(pattern4, test_text4)
    print(f"\n4. 从文本中提取整数")
    print(f"文本: '{test_text4}'")
    print(f"提取的整数: {integers}")
    
    # 5. 有效的文件路径（带扩展名）
    pattern5 = r'^(/[^/ ]*)+\.(txt|csv|jpg|png|pdf|doc|docx|xls|xlsx)$'
    test_cases5 = ['/home/user/file.txt', '/tmp/image.jpg', 'report.doc', '/invalid path/file.txt']
    expected5 = [True, True, False, False]  # 'report.doc'没有完整路径
    results5 = test_regex(pattern5, test_cases5, expected5)
    print_test_results(results5, "5. 有效的文件路径（带扩展名）")
    
    # 6. 加拿大邮政编码（格式：A1A 1A1）
    pattern6 = r'^[A-Za-z]\d[A-Za-z]\s\d[A-Za-z]\d$'
    test_cases6 = ['K1A 0B1', '123 456', 'M5V 2H1']
    expected6 = [True, False, True]
    results6 = test_regex(pattern6, test_cases6, expected6)
    print_test_results(results6, "6. 加拿大邮政编码")
    
    # 7. 首尾字符相同的字符串
    pattern7 = r'^(.).*\1$|^.$'  # 修改为允许单个字符的情况
    test_cases7 = ['level', 'stats', 'world', 'a', 'aa']
    expected7 = [True, True, False, True, True]  # 单个字符也算首尾相同
    results7 = test_regex(pattern7, test_cases7, expected7)
    print_test_results(results7, "7. 首尾字符相同的字符串")
    
    # 8. 强密码验证
    # 至少一个大写字母，一个小写字母，一个数字，一个特殊字符，最小长度10
    pattern8 = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{10,}$'
    test_cases8 = ['Secure123!', 'weakpass', 'ValidPass#2023', 'Short1!']
    expected8 = [True, False, True, False]  # 'Short1!'长度不足10
    results8 = test_regex(pattern8, test_cases8, expected8)
    print_test_results(results8, "8. 强密码验证")
    
    # 9. 日期提取（mm/dd/yyyy 或 yyyy-mm-dd）
    pattern9 = r'^((0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4})|(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'
    test_cases9 = ['07/04/2021', '2022-12-31', '2022/12/31', '13-2020', '07-04-21']
    expected9 = [True, True, False, False, False]
    results9 = test_regex(pattern9, test_cases9, expected9)
    print_test_results(results9, "9. 日期格式验证")
    
    # 10. 有效的IPv6地址
    pattern10 = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    test_cases10 = ['2001:0db8:85a3:0000:0000:8a2e:0370:7334', '1234:5678:90ab:cdef:ghij:0000:0000:0001']
    expected10 = [True, False]  # 第二个包含非十六进制字符ghij
    results10 = test_regex(pattern10, test_cases10, expected10)
    print_test_results(results10, "10. 有效的IPv6地址")
    
    # 总结所有正则表达式模式
    print("\n" + "=" * 80)
    print("所有正则表达式模式汇总：")
    print("=" * 80)
    print(f"1. 仅包含字母的字符串: {pattern1}")
    print(f"2. 以辅音开头的单词: {pattern2}")
    print(f"3. 有效的域名: {pattern3}")
    print(f"4. 提取整数: {pattern4}")
    print(f"5. 有效的文件路径: {pattern5}")
    print(f"6. 加拿大邮政编码: {pattern6}")
    print(f"7. 首尾字符相同的字符串: {pattern7}")
    print(f"8. 强密码验证: {pattern8}")
    print(f"9. 日期格式验证: {pattern9}")
    print(f"10. 有效的IPv6地址: {pattern10}")


if __name__ == "__main__":
    main()