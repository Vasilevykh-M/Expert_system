import json

def save_logs(database_name, tree_view, work_memory):
  with open("logs.json") as file:
      data = json.load(file)
      for i in data:
        if i["file_name"] == database_name:
          i["file_name"] = database_name
          i["value"] = {
              "tree_view": tree_view,
              "work_memory": work_memory
          }
          return data
      data.append({"file_name": database_name, "value": {
              "tree_view": tree_view,
              "work_memory": work_memory
          }})
      return data

def save_logs_(data):
  with open("logs.json", 'w') as f:
      json.dump(data, f)

def load_logs():
    with open("logs.json") as file:
        data = json.load(file)
        return data