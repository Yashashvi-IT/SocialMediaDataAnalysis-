#!/usr/bin/env python
# coding: utf-8

# # Clean & Analyze Social Media

# ## Introduction
# 
# Social media has become a ubiquitous part of modern life, with platforms such as Instagram, Twitter, and Facebook serving as essential communication channels. Social media data sets are vast and complex, making analysis a challenging task for businesses and researchers alike. In this project, we explore a simulated social media, for example Tweets, data set to understand trends in likes across different categories.
# 
# ## Prerequisites
# 
# To follow along with this project, you should have a basic understanding of Python programming and data analysis concepts. In addition, you may want to use the following packages in your Python environment:
# 
# - pandas
# - Matplotlib
# - ...
# 
# These packages should already be installed in Coursera's Jupyter Notebook environment, however if you'd like to install additional packages that are not included in this environment or are working off platform you can install additional packages using `!pip install packagename` within a notebook cell such as:
# 
# - `!pip install pandas`
# - `!pip install matplotlib`
# 
# ## Project Scope
# 
# The objective of this project is to analyze tweets (or other social media data) and gain insights into user engagement. We will explore the data set using visualization techniques to understand the distribution of likes across different categories. Finally, we will analyze the data to draw conclusions about the most popular categories and the overall engagement on the platform.
# 
# ## Step 1: Importing Required Libraries
# 
# As the name suggests, the first step is to import all the necessary libraries that will be used in the project. In this case, we need pandas, numpy, matplotlib, seaborn, and random libraries.
# 
# Pandas is a library used for data manipulation and analysis. Numpy is a library used for numerical computations. Matplotlib is a library used for data visualization. Seaborn is a library used for statistical data visualization. Random is a library used to generate random numbers.

# In[2]:


# ========================================
# Social Media Data Analysis Project
# ========================================

# ----------------------------------------
# Step 1: Import Libraries
# ----------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import re
from datetime import datetime

# ----------------------------------------
# Step 2: Create / Load Dataset
# ----------------------------------------
# If you have a dataset file, replace with:
# df = pd.read_csv("tweets.csv")

categories = ['fitness','tech','family','beauty','food','health','travel','education']
n = 500  # number of posts to simulate

random.seed(42)
np.random.seed(42)

def fake_text(cat):
    samples = {
        'fitness': ["Morning workout done! 💪", "5 tips to build stamina"],
        'tech': ["New AI library released", "How to optimize your pipeline"],
        'family': ["Family dinner memories", "Parenting tips for toddlers"],
        'beauty': ["Skincare routine for glowing skin", "Top makeup trends 2025"],
        'food': ["Tried this pasta recipe — yum!", "Top 5 street foods"],
        'health': ["Mental health matters", "Healthy meals under 500 cal"],
        'travel': ["Hidden beaches in Goa", "Backpacking on a budget"],
        'education': ["How to learn Python fast", "Study tips for exams"]
    }
    return random.choice(samples[cat])

data = []
base_date = datetime(2025,1,1)
for i in range(n):
    cat = random.choice(categories)
    created = base_date + pd.to_timedelta(random.randint(0,250), unit='D')
    likes = max(0, int(np.random.poisson(lam=50) + (10 if cat in ['food','tech'] else 0) + random.randint(-5,20)))
    retweets = max(0, int(np.random.poisson(lam=8)))
    text = fake_text(cat)
    data.append({
        'id': i+1,
        'text': text,
        'category': cat,
        'created_at': created.isoformat(),
        'likes': likes,
        'retweets': retweets
    })

df = pd.DataFrame(data)

# ----------------------------------------
# Step 3: Data Cleaning
# ----------------------------------------
def clean_text(s):
    if pd.isna(s):
        return ""
    s = re.sub(r'http\S+', '', s)            # remove URLs
    s = re.sub(r'@\w+', '', s)               # remove mentions
    s = re.sub(r'#[A-Za-z0-9_]+', '', s)     # remove hashtags
    s = re.sub(r'[^\x00-\x7F]+',' ', s)      # remove emojis/non-ASCII
    s = re.sub(r'\s+', ' ', s).strip()
    return s

df['text_clean'] = df['text'].apply(clean_text)
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0).astype(int)
df['retweets'] = pd.to_numeric(df['retweets'], errors='coerce').fillna(0).astype(int)

# Remove duplicates
df = df.drop_duplicates(subset=['text_clean','created_at']).reset_index(drop=True)

# Handle missing categories
df['category'] = df['category'].fillna('unknown')

print("Dataset shape:", df.shape)
print("\nSample rows:")
print(df.head().to_string(index=False))

# ----------------------------------------
# Step 4: Aggregated Analysis
# ----------------------------------------
likes_by_cat = df.groupby('category')['likes'].agg(['count','sum','mean','median']).reset_index().sort_values('sum', ascending=False)
print("\nLikes by category:")
print(likes_by_cat.to_string(index=False))

# ----------------------------------------
# Step 5: Visualizations
# ----------------------------------------
plt.figure(figsize=(8,5))
sns.barplot(data=likes_by_cat, x='category', y='sum')
plt.xticks(rotation=45)
plt.title('Total Likes per Category')
plt.xlabel('Category')
plt.ylabel('Total Likes')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='category', y='likes')
plt.xticks(rotation=45)
plt.title('Likes Distribution by Category')
plt.tight_layout()
plt.show()

# ----------------------------------------
# Step 6: Category Filtering Example
# ----------------------------------------
selected = df[df['category'].isin(['food','tech'])]
print("\nFiltered (food + tech) count:", selected.shape[0])

# ----------------------------------------
# Step 7: Simple Performance Recommendations
# ----------------------------------------
overall_mean = df['likes'].mean()
likes_by_cat['status'] = likes_by_cat['mean'].apply(
    lambda m: 'performing well' if m > overall_mean*1.1 else ('underperforming' if m < overall_mean*0.9 else 'average')
)

print("\nCategory Performance Status:")
print(likes_by_cat[['category','mean','status']].to_string(index=False))

# ----------------------------------------
# Step 8: Save Cleaned Data (Optional)
# ----------------------------------------
# df.to_csv("tweets_cleaned.csv", index=False)

# ========================================
# END OF NOTEBOOK
# ========================================


# In[ ]:




