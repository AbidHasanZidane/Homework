using System;
using System.Windows.Forms;
using System.Timers;
using static System.Net.Mime.MediaTypeNames;
using System.Reflection.Emit;
using System.Reflection;

public class AlarmClockForm : Form
{
    private System.Windows.Forms.Label lblTime;
    private System.Windows.Forms.Label lblStatus;
    private Button btnSetAlarm;
    private DateTimePicker dtpAlarmTime;

    private System.Timers.Timer timer;
    private DateTime alarmTime;
    private bool alarmSet = false;

    public AlarmClockForm()
    {
        // Properties of the form
        this.Text = "WinForms Alarm Clock";
        this.Size = new System.Drawing.Size(400, 200);

        // Showing clock
        lblTime = new System.Windows.Forms.Label() { Text = "Current Time: ", AutoSize = true, Top = 20, Left = 20 };
        this.Controls.Add(lblTime);

        // Label below current time
        lblStatus = new System.Windows.Forms.Label() { Text = "Status: Waiting for alarm...", AutoSize = true, Top = 50, Left = 20 };
        this.Controls.Add(lblStatus);

        // DateTime Picker
        dtpAlarmTime = new DateTimePicker() { Format = DateTimePickerFormat.Time, ShowUpDown = true, Top = 80, Left = 20 };
        this.Controls.Add(dtpAlarmTime);

        // Set Alarm Button
        btnSetAlarm = new Button() { Text = "Set Alarm", Top = 110, Left = 20 };
        btnSetAlarm.Click += BtnSetAlarm_Click;
        this.Controls.Add(btnSetAlarm);

        // Timer Setup
        timer = new System.Timers.Timer(500); // interval set for half second
        timer.Elapsed += OnTick;
        timer.Start();
    }

    private void BtnSetAlarm_Click(object sender, EventArgs e)
    {
        alarmTime = dtpAlarmTime.Value;
        alarmSet = true;
        lblStatus.Text = $"Alarm Set for: {alarmTime:HH:mm:ss}";
    }

    private void OnTick(object sender, ElapsedEventArgs e)
    {
        this.Invoke((MethodInvoker)delegate {
            lblTime.Text = $"Current Time: {DateTime.Now:HH:mm:ss}";

            if (alarmSet && DateTime.Now.Hour == alarmTime.Hour &&
                DateTime.Now.Minute == alarmTime.Minute &&
                DateTime.Now.Second == alarmTime.Second)
            {
                alarmSet = false;
                lblStatus.Text = "Alarm Ringing!";

                // Will show message box and wait for user action
                MessageBox.Show("Alarm is ringing!", "Alarm", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // Will reset status label after the message box is closed
                lblStatus.Text = "Status: Waiting for alarm...";
            }
        });
    }

    [STAThread]
    public static void Main()
    {
        System.Windows.Forms.Application.EnableVisualStyles();
        System.Windows.Forms.Application.Run(new AlarmClockForm());
    }
}
