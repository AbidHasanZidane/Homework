using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace SearchInfo
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private async void button1_Click(object sender, EventArgs e)
        {
            string keyword = textBox.Text.Trim();
            if (string.IsNullOrEmpty(keyword)) return;

            button1.Enabled = false;
            progressBar.Visible = true;
            progressBar.Value = 10;

            showData.Clear();
            showData2.Clear();
            showData.Text = "搜索中...";
            showData2.Text = "搜索中...";

            try
            {
                var results = await SearchBingAsync(keyword);
                progressBar.Value = 80;

                showData.Text = results.Length > 0 ? results[0] : "搜素失败";
                showData2.Text = results.Length > 1 ? results[1] : "搜索失败";

                progressBar.Value = 100;
            }
            catch (Exception ex)
            {
                showData.Text = "异常: " + ex.Message;
                showData2.Text = "";
                progressBar.Value = 0;
            }

            await Task.Delay(500); 
            progressBar.Visible = false;
            button1.Enabled = true;
        }


        private async Task<string[]> SearchBingAsync(string keyword)
        {
            using HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64)");

            string url = $"https://www.bing.com/search?q={Uri.EscapeDataString(keyword)}";
            string html = await client.GetStringAsync(url);

           
            File.WriteAllText("bing_debug.html", html);

            
            var matches = Regex.Matches(html, @"<li class=""b_algo"".*?<p.*?>(.*?)</p>", RegexOptions.Singleline);
            var results = new List<string>();

            foreach (Match match in matches)
            {
                string text = Regex.Replace(match.Groups[1].Value, "<.*?>", "");
                text = System.Net.WebUtility.HtmlDecode(text); 

                if (!string.IsNullOrWhiteSpace(text))
                {
                    results.Add(text.Length > 400 ? text.Substring(0, 400) : text);
                    if (results.Count == 2)
                        break;
                }
            }

            return results.ToArray();
        }



        private void saveToFile_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveDialog = new SaveFileDialog();
            saveDialog.Filter = "Text Files (*.txt)|*.txt";
            saveDialog.Title = "保存搜索结果";

            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    File.WriteAllText(saveDialog.FileName,
                        "结果1:\r\n" + showData.Text + "\r\n\r\n结果2:\r\n" + showData2.Text);
                    MessageBox.Show("保存成功！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("保存失败: " + ex.Message, "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void textBox_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void showData_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void progressBar_Click(object sender, EventArgs e)
        {
            
        }
    }
}
