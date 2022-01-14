from decouple import config
connection_string = f'mongodb://{config("USER")}:{config("PASSWORD")}@{config("HOST")}/?authSource={config("DATABASE")}&{config("MONGODB_OPTIONS")}'