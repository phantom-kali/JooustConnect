# JooustConnect

JooustConnect is a Django-based application designed to facilitate social networking and communication within a community. The application includes features for managing groups, messaging, notifications, and user profiles.

## Features

- **Groups**: Create and manage groups, view group details, and handle group requests.
- **Messaging**: Send and receive messages within the platform.
- **Notifications**: Receive and manage notifications related to user activities.
- **User Profiles**: Manage user profiles, including profile pictures and premium features.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/phantom-kali/JooustConnect.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd JooustConnect
   ```

3. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Use the admin interface to manage groups, users, and notifications.

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -am 'Add new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [fideleliudclimax@gmail.com](mailto:fideleliudclimax@gmail.com).
