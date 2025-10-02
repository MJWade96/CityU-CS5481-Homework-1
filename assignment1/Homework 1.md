# CS5481: Data Engineering – Assignment 1

## Instructions

1. **Due on**: Wednesday, October 8, 2025, 18:00:00 PM  
2. **Submission format**:  
   - A single PDF with the code package, **or**  
   - A single Jupyter Notebook containing both answers and code  
3. For coding questions:  
   - Include code **and** descriptions of your code design and workflow  
   - Provide detailed analysis of experimental results where applicable  
4. **Total marks**: 100  
5. **Plagiarism or unjustified late submission** will result in invalidation or point deduction  
6. Questions? Post them on the **Canvas Discussion forum**

---

## Question 1 – Online Reviews Data Collection (20 marks)

User-generated reviews on e-commerce and entertainment platforms provide valuable information for text mining and sentiment analysis. However, obtaining high-quality review data can be challenging, especially when official APIs are limited or restricted. In such cases, **web scraping** can be used to collect data directly from websites.

### Task:
Collect **30 online user reviews** from the websites listed below and prepare them for analysis.

### Requirements:
1. Each entry must include:
   - **Review text**
   - At least **one associated reply or rating** (e.g., helpfulness votes, star rating, or comment)
2. **Only textual and numerical information** – ignore images, videos, or other multimedia
3. Store data in a **structured format** (e.g., JSON or CSV) with fields such as:
   - `review_text`
   - `user`
   - `date`
   - `rating`
   - `reply` / `comment`

### Suggested Sources:
- [IMDb](https://www.imdb.com) (movie reviews)  
- [Goodreads](https://www.goodreads.com) (book reviews)  
- [TripAdvisor](https://www.tripadvisor.com) (travel reviews)  
- [Amazon](https://www.amazon.com) (product reviews)

> **Deliverable**: Submit your code and the structured dataset.

---

## Question 2 – Data Cleaning with Regular Expressions (30 marks)

Regular Expressions (Regex) are powerful tools for searching, validating, and transforming text data during preprocessing.

### Tasks:
Write the appropriate **regex pattern in Python** for each of the following:

1. **Alphabetic-only string**  
   - Valid: `Python`, `DataScience`  
   - Invalid: `Hello123`

2. **Words beginning with a consonant**  
   - Test words: `cat`, `elephant`, `dog`, `owl`

3. **Valid domain name** (e.g., `example.com`)  
   - Valid: `openai.org`, `my-site.net`  
   - Invalid: `invalid@site`

4. **Extract all integers** from text  
   - Example: `"He scored 45 goals in 2022 and 10 goals in 2023."`

5. **Valid file paths with extensions** (e.g., `.txt`, `.csv`, `.jpg`)  
   - Valid: `/home/user/file.txt`, `/tmp/image.jpg`  
   - Invalid: `report.doc` (if `.doc` not considered valid — clarify if needed)

6. **Canadian postal code** (format: `A1A 1A1`)  
   - Valid: `K1A 0B1`  
   - Invalid: `123 456`

7. **Strings where first and last characters are identical**  
   - Valid: `level`, `stats`  
   - Invalid: `world`

8. **Strong password validation**:  
   Must contain:
   - At least one uppercase letter  
   - One lowercase letter  
   - One digit  
   - One special character  
   - Minimum length: 10  
   - Test cases: `Secure123!`, `weakpass`, `ValidPass#2023`

9. **Date extraction** in either format:
   - `mm/dd/yyyy` (e.g., `07/04/2021`)  
   - `yyyy-mm-dd` (e.g., `2022-12-31`)  
   - **Invalid**: `2022/12/31`, `13-2020`, `07-04-21`

10. **Valid IPv6 address**  
    - Valid: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`  
    - Invalid: `1234:5678:90ab:cdef:ghij:0000:0000:0001` (contains non-hex `ghij`)

> **Deliverable**: Submit regex patterns with test code.

---

## Question 3 – Data Processing (20 marks)

Machine translation datasets are often in **XML format**. Before training, we convert them to **line-based plain text**.

### Tasks:

1. **Convert XML to line-based text**  
   - Source file: [`sample-hyp.xml`](https://github.com/wmt-conference/wmt-format-tools/tree/main/test/sample-data/sample-hyp.xml)  
   - Requirements:
     - Remove all **punctuation**
     - Convert all text to **lowercase**
   - Deliverable: Runnable Python code + output text file

2. **Build a BPE vocabulary**  
   - Use the tool: [`subword-nmt`](https://github.com/rsennrich/subword-nmt.git)  
   - Output: One BPE token per line  
   - Deliverable: Code to run BPE + resulting vocabulary file

---

## Question 4 – Data Visualization (30 marks)

### Part (a)
You have a dataset of **500 students** with:
- `Student ID`: Integer (1–500)  
- `Major`: Categorical (`Computer Science`, `Mathematics`, `Physics`)  
- `Gender`: Binary (`Male`/`Female`)  
- `GPA`: Continuous (0.0–4.0)

> **Question**: Which visualization methods are appropriate to explore:
> - Distribution of each attribute?  
> - Relationships between attributes?

### Part (b)
- **Generate** 500 random student records in Python  
- **Visualize** using the methods selected in (a)

### Part (c)
- Compute **number of students per major**  
- Display using a **bar chart**

### Part (d)
In recommendation systems, similarity between user and item embeddings can be computed as:

\[
\text{Similarity}(U, V) = \text{softmax}\left(\frac{U V^T}{\sqrt{d}}\right)
\]

Where:
- \( U \in \mathbb{R}^{5 \times 8} \): user embeddings  
- \( V \in \mathbb{R}^{5 \times 8} \): item embeddings  
- \( d = 8 \): embedding dimension

> **Task**:  
> - Randomly initialize \( U \) and \( V \)  
> - Compute similarity matrix  
> - Visualize using a **heatmap**

> **Deliverable**: Python code + visualizations