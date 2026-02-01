import asyncio
import argparse
import os
import sys
from gpt_researcher import GPTResearcher

# === 🛡️ COST & CONFIGURATION GUARD ===
# 强制配置以确保使用低成本模型，并优化搜索策略

def configure_env():
    """Ensure the environment is set up for low-cost research."""
    
    # 1. 设置搜索引擎 (Tavily 对 Agent 最友好)
    os.environ["RETRIEVER"] = "tavily"
    
    # 2. 强制设置 LLM 模型
    # 优先检测 Gemini (Flash 模型性价比最高)，如果没配置则回退
    if os.getenv("GEMINI_API_KEY"):
        print("✅ Configured: Using Google Gemini (Low Cost Mode)")
        os.environ["FAST_LLM"] = "google_gemini"
        os.environ["SMART_LLM"] = "google_gemini" 
    elif os.getenv("OPENAI_API_KEY"):
        print("⚠️ Warning: GEMINI_API_KEY not found. Using OpenAI (Check your costs).")
        # 如果是 OpenAI，建议用户在环境变量里配置模型为 gpt-4o-mini
    else:
        print("❌ Critical Error: No API Key (Gemini or OpenAI) found.")
        sys.exit(1)

async def main():
    parser = argparse.ArgumentParser(description="Deep Research Worker Agent")
    parser.add_argument("--query", type=str, required=True, help="The research objective")
    parser.add_argument("--filename", type=str, default="research_output.md", help="Output filename")
    parser.add_argument("--report_type", type=str, default="research_report", help="Type of report")
    
    args = parser.parse_args()

    print(f"\n🚀 STARTING WORKER: {args.query}")
    print(f"📄 Output Target: {args.filename}")

    try:
        # 初始化 Researcher
        researcher = GPTResearcher(query=args.query, report_type=args.report_type)
        
        # 1. 执行搜索与研究
        print("🔍 Searching, Scraping & Reading (Please wait)...")
        await researcher.conduct_research()
        
        # 2. 撰写报告正文
        print("✍️ Synthesizing Report...")
        report_content = await researcher.write_report()
        
        # 3. 关键步骤：提取并追加权威数据源链接
        print("🔗 Extracting Sources...")
        source_urls = researcher.get_source_urls()
        
        sources_section = "\n\n## 📚 权威参考资料 / Verified Data Sources\n"
        sources_section += "> **Note to Agent:** When rewriting, you MUST verify data against these links.\n\n"
        for url in source_urls:
            sources_section += f"- {url}\n"
            
        final_output = report_content + sources_section
        
        # 4. 保存文件
        with open(args.filename, "w", encoding="utf-8") as f:
            f.write(final_output)
            
        print(f"✅ DONE. Report with citations saved to {args.filename}")
        print(f"📊 Total Sources Found: {len(source_urls)}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    configure_env()
    asyncio.run(main())
