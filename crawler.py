import requests
from bs4 import BeautifulSoup
import json
import datetime
from pathlib import Path

# 替换为真实的英雄联盟赛程官网地址（示例地址，需根据实际调整）
TARGET_URL = "https://lpl.qq.com/es/schedule.shtml"

def crawl_schedule():
    try:
        # 1. 发送请求（模拟浏览器）
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://lpl.qq.com/",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        # 2. 解析页面（适配英雄联盟官网结构，若官网结构不同需微调）
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []
        
        # 示例：适配英雄联盟赛事官网的赛程选择器（需根据实际DOM调整）
        match_items = soup.select(".match-item, .match-list-item, .game-item")
        if not match_items:
            # 若无数据，使用默认赛程（防止页面空白）
            generate_default_matches()
            return

        for idx, item in enumerate(match_items):
            try:
                # 提取核心信息（根据官网DOM调整选择器）
                date = item.select_one(".match-date, .date").text.strip() if item.select_one(".match-date, .date") else f"2026-03-{16+idx%7}"
                time = item.select_one(".match-time, .time").text.strip() if item.select_one(".match-time, .time") else "21:00"
                stage = item.select_one(".match