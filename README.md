# Jigsaw-Comments-Severity-Rating-Application

This project aims to create a machine learning model that rates the severity of comments based on the dataset provided by the Jigsaw-Rate Severity of Toxic Comments Kaggle competition. Additionally, it provides a user-friendly web interface to input comments and view their corresponding scores. The project is implemented using Python and Streamlit framework, with data storage in a MySQL database. Analytical charts are generated using Matplotlib and Pandas libraries.

## Features

- Machine learning model: The ML model is trained on the Jigsaw competition dataset to accurately rate the severity of comments.
- Web interface: A user-friendly web interface is provided to interact with the ML model. Users can input comments and receive the corresponding severity scores.
- MySQL integration: The project enables storing user-entered comments and their calculated scores in a MySQL database for further analysis.
- Analytical charts: Matplotlib and Pandas libraries are utilized to generate insightful charts based on the stored data, providing visual representations of comment severity trends.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/comment-rating-ml-model.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the MySQL database:

- Create a new MySQL database.
- Update the database connection details in the `config.py` file.

4. Run the application:

```bash
streamlit run app.py
```

5. Access the web interface:

Open your web browser and visit `http://localhost:8501` to access the application.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test thoroughly.
5. Commit your changes and push to your forked repository.
6. Submit a pull request, describing your changes in detail.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The Jigsaw-Rate Severity of Toxic Comments Kaggle competition for providing the dataset.
- Streamlit, Matplotlib, Pandas, and MySQL for the libraries used in the project.

Feel free to modify and expand this README file to include any additional details or instructions specific to your project.
