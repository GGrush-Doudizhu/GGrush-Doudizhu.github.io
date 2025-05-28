import csv
import os
from collections import defaultdict


def process_sponsor_data():
    # --- Path Setup ---
    # Get the absolute path of the current script
    script_abspath = os.path.abspath(__file__)
    # Get the directory of the script: D:\MyGitHubWebsite\GGrush-Doudizhu.github.io\scripts
    script_dir = os.path.dirname(script_abspath)
    # Get the project root directory: D:\MyGitHubWebsite\GGrush-Doudizhu.github.io
    project_root = os.path.dirname(script_dir)

    # Define input and output file paths
    input_csv_path = os.path.join(project_root, "sponsor", "details", "donate_list.csv")
    output_csv_path = os.path.join(project_root, "sponsor", "details", "donate_sort.csv")
    output_html_path = os.path.join(project_root, "sponsor", "sponsor_display_html_script_part.html")

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    # --- Requirement 1: Aggregate and sort sponsor data ---
    sponsor_totals = defaultdict(float)

    try:
        with open(input_csv_path, mode='r', encoding='utf-8-sig') as infile:  # utf-8-sig handles BOM
            reader = csv.DictReader(infile)
            if not reader.fieldnames or '赞助者' not in reader.fieldnames or '金额' not in reader.fieldnames:
                print(f"错误：CSV文件 {input_csv_path} 缺少必要的列名 ('赞助者', '金额') 或为空。")
                return

            for row in reader:
                sponsor_name = row.get('赞助者', '').strip()
                amount_str = row.get('金额', '0').strip()

                if not sponsor_name:  # Skip if sponsor name is empty
                    print(f"警告：发现空赞助者名称，行数据: {row}")
                    continue

                try:
                    amount = float(amount_str)
                    sponsor_totals[sponsor_name] += amount
                except ValueError:
                    print(f"警告：无法将金额 '{amount_str}' 转换为数字，赞助者: {sponsor_name}，行数据: {row}")
                    continue

    except FileNotFoundError:
        print(f"错误：输入文件 {input_csv_path} 未找到。")
        return
    except Exception as e:
        print(f"读取CSV文件时发生错误: {e}")
        return

    if not sponsor_totals:
        print("未从CSV文件中读取到任何有效的赞助数据。")
        return

    # Sort sponsors by total amount in descending order
    sorted_sponsors = sorted(sponsor_totals.items(), key=lambda item: item[1], reverse=True)

    # Write sorted data to donate_sort.csv
    try:
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['赞助者', '总金额'])  # Header
            for name, total in sorted_sponsors:
                writer.writerow([name, f"{total:.2f}"])  # Format amount to 2 decimal places
        print(f"赞助者总金额已成功保存到: {output_csv_path}")
    except Exception as e:
        print(f"写入 {output_csv_path} 时发生错误: {e}")

    # --- Requirement 2: Generate HTML snippet ---
    html_content = []
    html_content.append('        <div class="featured-sponsors-grid">')

    for i, (name, total) in enumerate(sorted_sponsors):
        # The image path 'sponsor/profile/SPONSOR_NAME.jpg' is relative to the root of your website
        # where the main HTML file (that includes this snippet) is located.
        # For example, if your site is at GGrush-Doudizhu.github.io/index.html,
        # then 'sponsor/profile/DBS.jpg' resolves to
        # GGrush-Doudizhu.github.io/sponsor/profile/DBS.jpg
        # Assuming avatar images are JPGs and named exactly as the sponsor.
        # You might need to adjust extensions or handle missing images if necessary.
        avatar_path = f"sponsor/profile/{name}.jpg"  # Change .jpg if avatars are different format

        # Adding a simple comment to indicate rank (optional)
        html_content.append(f'            <!-- {i + 1}. {name} - Total: {total:.2f} -->')
        html_content.append('            <div class="sponsor-profile">')
        html_content.append('                <div class="sponsor-avatar-wrapper">')
        html_content.append(f'                    <img src="{avatar_path}" alt="{name}">')
        html_content.append('                </div>')
        html_content.append(f'                <span class="sponsor-name">{name}</span>')
        html_content.append('            </div>')

    html_content.append('        </div>')

    try:
        with open(output_html_path, mode='w', encoding='utf-8') as outfile:
            outfile.write("\n".join(html_content))
        print(f"HTML代码片段已成功保存到: {output_html_path}")
    except Exception as e:
        print(f"写入 {output_html_path} 时发生错误: {e}")


if __name__ == '__main__':
    process_sponsor_data()