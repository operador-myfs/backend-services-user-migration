import requests
from app import create_app

app = create_app()


if __name__ == "__main__":  # Only in dev
    citizen = {
      "id": 12222222221,
      "name": "Carlos Andres Caro",
      "address": "Cra 54 # 45 -67",
      "email": "caro@mymail.com",
      "operatorId": "66ca18cd66ca9f0015a8afb3",
      "operatorName": "Nsync"
    }
    #response = requests.post('https://govcarpeta-apis-83e1c996379d.herokuapp.com/apis/registerCitizen')
    app.run(host="0.0.0.0", port=8080, debug=True)  # nosec
