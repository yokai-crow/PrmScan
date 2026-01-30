# PrmScan

**PrmScan** is a lightweight Linux permission anomaly detector that helps identify risky file permissions in critical system directories. This tool scans directories for files with potentially unsafe permissions and provides suggestions on how to secure them.

## ⚠️ WARNING

**This tool is currently under active development and testing. Please use with caution and verify results in your sandbox environment.**


## Features

- **Scan Directories**: Checks permissions for files in default system directories or any directories specified by the user.
- **Real-Time Monitoring**: Monitors directories for file modifications or new file creations, reporting risky permission changes in real-time.
- **Risk Scoring**: Each file is assigned a risk score based on its permissions, with suggestions to mitigate risks.
- **Generate JSON Reports**: Saves a detailed JSON report of all files with risky permissions.

## Installation

### 1. Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/yokai-crow/PrmScan.git
cd permission-scanner
```

### 2. Install Dependencies

Make sure you have Python 3 installed. Then, install the required dependencies with the following command:

```bash
pip install -r requirements.txt
```

This will install all the required packages, such as `watchdog`, which is necessary for real-time file monitoring.

### 3. Install PrmScan Globally (Optional)

You can install PrmScan globally on your system so that you can run it like any other command-line tool.

To install PrmScan globally, use the following command:

```bash
pip install .
```

This will install PrmScan and allow you to run it from anywhere on your system.

## Running PrmScan

Once the tool is installed, you can run it directly from the command line.

### 1. Running PrmScan Using Python

If you prefer not to install it globally, you can always run the tool directly using Python. From the project directory, run:

```bash
python prmscan.py
```

### 2. Running PrmScan Globally (After Installation)

Once installed globally, you can run PrmScan from anywhere on your system. Some common commands are:

- **Scan Specific Directories:**

  ```bash
  prmscan -d /home /etc /var
  ```

- **Generate a JSON Report:**

  ```bash
  prmscan -r
  ```

  The report will be saved as `prmscan_report.json`.

- **Monitor Directories in Real-Time:**

  ```bash
  prmscan -m
  ```

  This will monitor specified directories for risky file changes and alert you in real-time.

## Command-Line Options

- `-d` : Scan specified directories for risky permissions.
  - Example: `prmscan -d /home /etc`
- `-r` : Generate a JSON report of all files with risky permissions.
  - Example: `prmscan -r`
- `-m` : Monitor directories in real-time for any permission changes.
  - Example: `prmscan -m`
- `-h` or `--help` : Display help information about available commands and options.

## Usage Example

When running the scan, if any files are found with risky permissions, they will be displayed with a risk score and a suggestion to mitigate the issue:

```
[ALERT] /home/user/suspicious_file.txt - Risk Score: 5
  -> Suggestion: Remove world write: chmod o-w
```

## Contributing

If you'd like to contribute to this project, feel free to fork it, make your changes, and submit a pull request. Any contributions, suggestions, or improvements are welcome.

### Steps to Contribute:

1. **Fork** the repository.
2. **Clone** your forked repository locally:

   ```bash
   git clone https://github.com/yokai-crow/PrmScan.git
   ```

3. **Create a new branch** for your changes:

   ```bash
   git checkout -b feature/your-feature
   ```

4. **Make your changes** and **commit** them:

   ```bash
   git commit -m "Added new feature"
   ```

5. **Push** your changes to your fork:

   ```bash
   git push origin feature/your-feature
   ```

6. **Create a pull request** with a detailed description of your changes.

## License

PrmScan is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.
