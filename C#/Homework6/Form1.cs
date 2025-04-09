using System;
using System.Net;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace WebCrawler
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            Load += Form1_Load;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Optional: preload a URL or set default UI state
        }

        private void txtResult_TextChanged(object sender, EventArgs e)
        {
            // You can leave this empty
        }

        private void txtUrl_TextChanged(object sender, EventArgs e)
        {
            // You can leave this empty
        }

        private void btnFetch_Click(object sender, EventArgs e)
        {
            string url = txtUrl.Text.Trim();

            if (string.IsNullOrEmpty(url))
            {
                MessageBox.Show("Please enter a URL.");
                return;
            }

            try
            {
                string html = "";

                using (WebClient client = new WebClient())
                {
                    client.Headers.Add("User-Agent", "Mozilla/5.0");

                    using (var stream = client.OpenRead(url))
                    using (System.IO.StreamReader reader = new System.IO.StreamReader(stream))
                    {
                        html = reader.ReadToEnd();
                    }
                }

                // Regular expressions
                string phonePattern = @"1[3-9]\d{9}";
                string emailPattern = @"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b";

                MatchCollection phoneMatches = Regex.Matches(html, phonePattern);
                MatchCollection emailMatches = Regex.Matches(html, emailPattern);

                txtResult.Clear();
                txtResult.AppendText("Phone Numbers:\r\n");

                foreach (Match match in phoneMatches)
                {
                    txtResult.AppendText(match.Value + "\r\n");
                }

                txtResult.AppendText("\r\nEmail Addresses:\r\n");

                foreach (Match match in emailMatches)
                {
                    txtResult.AppendText(match.Value + "\r\n");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message);
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtResult.Text))
            {
                MessageBox.Show("There is no result to save.", "No Data", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            using (SaveFileDialog saveDialog = new SaveFileDialog())
            {
                saveDialog.Title = "Save Extracted Data";
                saveDialog.Filter = "Text Files (*.txt)|*.txt|All Files (*.*)|*.*";
                saveDialog.FileName = "extractedData.txt";

                if (saveDialog.ShowDialog() == DialogResult.OK)
                {
                    try
                    {
                        System.IO.File.WriteAllText(saveDialog.FileName, txtResult.Text);
                        MessageBox.Show("Data saved successfully!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Error saving file: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

    }
}
