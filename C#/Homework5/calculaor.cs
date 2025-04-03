namespace Calcul
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        int num1;
        int num2;
        int result;
        string option;
        bool isOperatorPressed = false;
        bool isResultDisplayed = false; // Flag to track result display

        private void btn9_Click(object sender, EventArgs e) { HandleNumberInput("9"); }
        private void btn8_Click(object sender, EventArgs e) { HandleNumberInput("8"); }
        private void btn7_Click(object sender, EventArgs e) { HandleNumberInput("7"); }
        private void btn6_Click(object sender, EventArgs e) { HandleNumberInput("6"); }
        private void btn5_Click(object sender, EventArgs e) { HandleNumberInput("5"); }
        private void btn4_Click(object sender, EventArgs e) { HandleNumberInput("4"); }
        private void btn3_Click(object sender, EventArgs e) { HandleNumberInput("3"); }
        private void btn2_Click(object sender, EventArgs e) { HandleNumberInput("2"); }
        private void btn1_Click(object sender, EventArgs e) { HandleNumberInput("1"); }
        private void btnZero_Click(object sender, EventArgs e) { HandleNumberInput("0"); }

        private void HandleNumberInput(string number)
        {
            // If "Error" is displayed, reset as if AC was pressed.
            if (textDisplay.Text == "Error")
                btnAc_Click(null, null);

            if (isResultDisplayed)
            {
                textDisplay.Clear(); // Clear display if result was shown
                isResultDisplayed = false;
            }
            textDisplay.Text += number;
        }

        private void btnPlus_Click(object sender, EventArgs e) { HandleOperator("+"); }
        private void btnMinus_Click(object sender, EventArgs e) { HandleOperator("-"); }
        private void btnMulti_Click(object sender, EventArgs e) { HandleOperator("*"); }
        private void btnDiv_Click(object sender, EventArgs e) { HandleOperator("/"); }

        private void HandleOperator(string op)
        {
            // If "Error" is displayed, reset as if AC was pressed.
            if (textDisplay.Text == "Error")
            {
                btnAc_Click(null, null);
                textDisplay.Text = "0 " + op + " ";
                num1 = 0;
            }
            else
            {
                string[] parts = textDisplay.Text.Split(' ');

                if (isResultDisplayed) // Start new calculation if result was shown
                {
                    num1 = result;
                    textDisplay.Text = num1 + " " + op + " ";
                }
                else if (isOperatorPressed) // Replace existing operator only
                {
                    textDisplay.Text = textDisplay.Text.Substring(0, textDisplay.Text.Length - 2) + op + " ";
                }
                else if (parts.Length == 1) // Ensure only one operator can be added
                {
                    num1 = int.Parse(parts[0]);
                    textDisplay.Text += " " + op + " ";
                }
            }

            option = op;
            isOperatorPressed = true;
            isResultDisplayed = false;
        }





        private void btnEql_Click(object sender, EventArgs e)
        {
            string[] parts = textDisplay.Text.Split(' ');

            if (parts.Length == 3 && int.TryParse(parts[2], out num2))
            {
                switch (option)
                {
                    case "+": result = num1 + num2; break;
                    case "-": result = num1 - num2; break;
                    case "*": result = num1 * num2; break;
                    case "/":
                        if (num2 == 0)
                        {
                            textDisplay.Text = "Error";
                            isResultDisplayed = true;
                            return;
                        }
                        result = num1 / num2;
                        break;
                }

                textDisplay.Text = num1 + " " + option + " " + num2 + " = " + result;
                isOperatorPressed = false;
                isResultDisplayed = true; // Mark result as displayed
            }
        }

        private void btnAc_Click(object sender, EventArgs e)
        {
            textDisplay.Clear();
            num1 = 0;
            num2 = 0;
            result = 0;
            option = "";
            isOperatorPressed = false;
            isResultDisplayed = false;
        }
    }
}
