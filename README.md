# AutoMate Hub ⚡

**Automatic Invoice Generation & Email Automation**

AutoMate Hub is a powerful, locally-hosted tool designed for freelancers and small businesses to automate their invoicing workflow. It takes a simple CSV file, generates professional PDF invoices for each client, and automatically emails them instantly.


---

## 🚀 Key Features

*   **Bulk Processing**: Generate hundreds of PDF invoices from a single CSV upload in seconds.
*   **Automated Emailing**: Connects to SMTP to send personalized emails with attached invoices automatically.
*   **Professional Design**: Clean, modern invoice templates using ReportLab.
*   **Privacy First**: Runs locally. Data is processed in memory and temporary files are cleaned up. No database, no accounts.
*   **Modern UI**: Built with a responsive, deep-teal themed interface for a premium user experience.

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI
*   **Frontend**: HTML5, CSS3, Vanilla JavaScript
*   **PDF Generation**: ReportLab
*   **Data Processing**: Pandas
*   **Server**: Uvicorn


## 📦 Installation & Usage

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/automate-hub.git
    cd automate-hub
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    uvicorn app.main:app --reload
    ```

5.  **Open in Browser**
    Visit `http://127.0.0.1:8000` to start automating your invoices!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
