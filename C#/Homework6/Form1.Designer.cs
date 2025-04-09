namespace WebCrawler
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            txtUrl = new TextBox();
            txtResult = new TextBox();
            label2 = new Label();
            btnFetch = new Button();
            btnSave = new Button();
            SuspendLayout();
            // 
            // txtUrl
            // 
            txtUrl.Location = new Point(84, 113);
            txtUrl.Name = "txtUrl";
            txtUrl.Size = new Size(522, 35);
            txtUrl.TabIndex = 0;
            txtUrl.TextChanged += txtUrl_TextChanged;
            // 
            // txtResult
            // 
            txtResult.Location = new Point(84, 191);
            txtResult.Multiline = true;
            txtResult.Name = "txtResult";
            txtResult.ReadOnly = true;
            txtResult.Size = new Size(695, 300);
            txtResult.TabIndex = 1;
            txtResult.TextChanged += txtResult_TextChanged;
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(84, 70);
            label2.Name = "label2";
            label2.Size = new Size(98, 30);
            label2.TabIndex = 3;
            label2.Text = "Enter Url:";
            // 
            // btnFetch
            // 
            btnFetch.Location = new Point(632, 113);
            btnFetch.Name = "btnFetch";
            btnFetch.Size = new Size(147, 35);
            btnFetch.TabIndex = 4;
            btnFetch.Text = "Search";
            btnFetch.UseVisualStyleBackColor = true;
            btnFetch.Click += btnFetch_Click;
            // 
            // btnSave
            // 
            btnSave.Location = new Point(632, 529);
            btnSave.Name = "btnSave";
            btnSave.Size = new Size(147, 38);
            btnSave.TabIndex = 5;
            btnSave.Text = "Save to file";
            btnSave.UseVisualStyleBackColor = true;
            btnSave.Click += btnSave_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(12F, 30F);
            AutoScaleMode = AutoScaleMode.Font;
            BackgroundImage = (Image)resources.GetObject("$this.BackgroundImage");
            ClientSize = new Size(861, 614);
            Controls.Add(btnSave);
            Controls.Add(btnFetch);
            Controls.Add(label2);
            Controls.Add(txtResult);
            Controls.Add(txtUrl);
            MaximizeBox = false;
            Name = "Form1";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Form1";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtUrl;
        private TextBox txtResult;
        private Label label2;
        private Button btnFetch;
        private Button btnSave;
    }
}
