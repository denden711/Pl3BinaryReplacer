import os
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def process_file(file_path, file_identifier):
    try:
        with open(file_path, 'rb') as file:
            binary_content = file.read()

        binary_str = binary_content.decode('ISO-8859-1')
        if "x=000" in binary_str:
            modified_str = binary_str.replace("x=000", file_identifier)
            modified_binary_content = modified_str.encode('ISO-8859-1')

            with open(file_path, 'wb') as file:
                file.write(modified_binary_content)

            return f"置換成功: {file_path}"
        else:
            return f"文字列 'x=000' が見つかりませんでした: {file_path}"
    except Exception as e:
        return f"置換失敗: {file_path}, エラー: {str(e)}"

def replace_text():
    folder = folder_path.get()

    if not folder:
        messagebox.showerror("エラー", "フォルダを選択してください")
        return

    log_entries = []
    errors_occurred = False

    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.startswith('x=') and filename.endswith('.pl3'):
                file_path = os.path.join(root, filename)
                file_identifier = filename.split('.')[0]  # ファイル名から拡張子を除外し "x=数字" を取得

                log_entry = process_file(file_path, file_identifier)
                log_entries.append(log_entry)
                if "置換失敗" in log_entry:
                    errors_occurred = True

    log_path = os.path.join(folder, f"replace_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    try:
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write('\n'.join(log_entries))

        if errors_occurred:
            messagebox.showwarning("警告", f"処理中にエラーが発生しました。詳細はログファイルを確認してください: {log_path}")
        else:
            messagebox.showinfo("完了", f"フォルダ内のすべての .pl3 ファイルで置換処理が完了しました。ログファイル: {log_path}")
    except Exception as e:
        messagebox.showerror("ログファイルエラー", f"ログファイルの作成中にエラーが発生しました: {str(e)}")

def create_gui():
    app = tk.Tk()
    app.title("BinaryReplaceTool")

    global folder_path
    folder_path = tk.StringVar()

    tk.Label(app, text="フォルダを選択:").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(app, textvariable=folder_path, width=50).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(app, text="フォルダを選択", command=select_folder).grid(row=0, column=2, padx=10, pady=10)

    tk.Button(app, text="置換を実行", command=replace_text).grid(row=1, columnspan=3, padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    create_gui()
