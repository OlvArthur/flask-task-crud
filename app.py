from flask import Flask, request, jsonify
from models.task import Task

# __name__ = "__main__"
app = Flask(__name__ )


tasks: list[Task] = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    return  jsonify({'message': 'New task successfully created'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    return jsonify({'tasks': task_list, 'total_tasks': len(tasks)})

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task_by_id(id):
    for task in tasks:
        if task.id == id:
          return jsonify(task.to_dict())
        
    return jsonify({'message':'Not possible to find this activity'}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    update_data = request.get_json()
    for task in tasks:
        if task.id == id:
            task.title = update_data.get('title', task.title)
            task.description = update_data.get('description', task.description)
            task.completed = update_data.get('completed', task.completed)
            return jsonify({'message':'Task successfully updated'})
        
    return jsonify({'message': 'Not posssible to find this activity'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({'message': 'Task successfully deleted'}) 
        
    return jsonify({'message': 'Not possible to find this activity'}), 404

if __name__ == "__main__":
    app.run(debug=True)