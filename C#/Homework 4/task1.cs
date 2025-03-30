using System;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using System.Drawing;

public class FileMergerForm : Form
{
    private Button btnSelectFile1, btnSelectFile2, btnMerge;
    private TextBox txtFile1, txtFile2;
    private Label lblFile1, lblFile2;
    private GroupBox groupBox;

    public FileMergerForm()
    {
        //Properties of the form.
        this.Text = "文本文件合并器";
        this.Size = new Size(600, 300);
        this.FormBorderStyle = FormBorderStyle.FixedDialog;
        this.StartPosition = FormStartPosition.CenterScreen;
        this.BackColor = Color.WhiteSmoke;
        this.FormBorderStyle = FormBorderStyle.FixedSingle; 
        this.MaximizeBox = false;
        this.BackgroundImage = Image.FromFile("C:\\Users\\zidane\\Pictures\\Saved Pictures\\1110.jpg"); // Set image
        this.BackgroundImageLayout = ImageLayout.Stretch;

        groupBox = new GroupBox()
        {
            Text = "文件合并工具",
            Font = new Font("Arial", 12, FontStyle.Bold),
            ForeColor = Color.DarkBlue,
            Size = new Size(550, 180),
            Top = 20,
            Left = 20
        };

        
        lblFile1 = new Label() { Text = "文件 1:", Top = 30, Left = 20, Height = 25, AutoSize = true, Font = new Font("Arial", 10, FontStyle.Bold) };
        txtFile1 = new TextBox() { Top = 30, Left = 80, Width = 350, Height = 25, Font = new Font("Arial", 10) };
        btnSelectFile1 = new Button() { Text = "选择", Top = 28, Height = 25, Left = 450, Width = 80 };
        btnSelectFile1.Click += (s, e) => SelectFile(txtFile1);

        lblFile2 = new Label() { Text = "文件 2:", Top = 70, Left = 20, AutoSize = true, Font = new Font("Arial", 10, FontStyle.Bold) };
        txtFile2 = new TextBox() { Top = 70, Left = 80, Width = 350, Font = new Font("Arial", 10) };
        btnSelectFile2 = new Button() { Text = "选择", Top = 68, Height = 25, Left = 450, Width = 80 };
        btnSelectFile2.Click += (s, e) => SelectFile(txtFile2);

        
        btnMerge = new Button()
        {
            Text = "合并文件",
            Top = 120,
            Left = 200,
            Width = 150,
            Height = 30,
            Font = new Font("Arial", 12, FontStyle.Bold),
            BackColor = Color.LightBlue,
            FlatStyle = FlatStyle.Flat
        };
        btnMerge.Click += MergeFiles;

        
        groupBox.Controls.Add(lblFile1);
        groupBox.Controls.Add(txtFile1);
        groupBox.Controls.Add(btnSelectFile1);
        groupBox.Controls.Add(lblFile2);
        groupBox.Controls.Add(txtFile2);
        groupBox.Controls.Add(btnSelectFile2);
        groupBox.Controls.Add(btnMerge);
        groupBox.Parent = this;
        groupBox.BackColor = Color.Transparent;



        this.Controls.Add(groupBox);
    }

    private void SelectFile(TextBox txtBox)
    {
        using (OpenFileDialog ofd = new OpenFileDialog() { Filter = "文本文件 (*.txt)|*.txt" })
        {
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                txtBox.Text = ofd.FileName;
            }
        }
    }

    private void MergeFiles(object sender, EventArgs e)
    {
        if (string.IsNullOrWhiteSpace(txtFile1.Text) || string.IsNullOrWhiteSpace(txtFile2.Text))
        {
            MessageBox.Show("请选择两个有效的文本文件！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        try
        {
            string outputDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Data");
            Directory.CreateDirectory(outputDir); 

            string outputFile = Path.Combine(outputDir, "MergedFile.txt");

            
            var mergedContent = File.ReadLines(txtFile1.Text).Concat(File.ReadLines(txtFile2.Text));

            File.WriteAllLines(outputFile, mergedContent);

            MessageBox.Show($"合并完成！文件已保存到:\n{outputFile}", "成功", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show($"发生错误: {ex.Message}", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    [STAThread]
    public static void Main()
    {
        Application.EnableVisualStyles();
        Application.Run(new FileMergerForm());
    }
}
