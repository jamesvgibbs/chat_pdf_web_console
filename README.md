## Getting Started

1. Clone the repository:

 ```git clone TBD```

2. Change to the project directory:

 ```cd your-repository```

3. Create a virtual environment and activate:
```
python3 -m venv venv
source venv/bin/activate
```
4. Install the required dependencies:

 ```pip install -r requirements.txt```

5. Create a read directory and place a PDF in that location. 

6. Update the PDF_PATH variable to read your PDF file by changing the file path:

7. Run the app.py script to start the chatbot:
```python3 app.py```

    a. If you want to use the web browser version:
    ```python3 app.py --streamlit```

8. Enter your questions at the prompt, and the chatbot will provide answers based on the PDF content. To exit the chatbot, type 'quit' when prompted for a question.

9. When you're done, deactivate the virtual environment:
``` deactivate ```

pip freeze > requirements.txt