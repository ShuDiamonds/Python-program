import urllib.request, json

if __name__ == '__main__':
    url = "https://mydeskworkhealth.azurewebsites.net/cope-json.php?filename=test.json" 
    method = "POST"
    headers = {"Content-Type" : "application/json"}

    # PythonオブジェクトをJSONに変換する
    obj = {"id" : 1, "name" : "python","age":35} 
    json_data = json.dumps(obj).encode("utf-8")

    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)