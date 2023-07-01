class User:
    def __init__(self, name='Lovel', surname='Kukuljan', username='lk', password='lk', weather_station='Zagreb-Grič'): #predefined user and weather station location
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password    
        self.weather_station = weather_station

    def check_user(self, username, password):
        if self.username == username and self.password == password:
            return True
        else:
            return False

    def update_name(self, new_username):
        self.username = new_username
        print('Username successfully updated!')

    def update_password(self, new_password):
        self.password = new_password
        print('Password successfully updated!')