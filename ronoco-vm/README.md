# :snake: Ronoco-vm

Le module **ronovo-vm** est l'un des modules du projet [ronoco](../README.md). C'est un paquet ROS et une A     PI flask
proposant des services pour contrôler un robot sous ROS.

## :hammer: Installation

Depuis le dossier `ronoco-vm̀` réaliser un `pip install requirements.txt`.

Si l'installation échoue les paquets pip nécessaires sont : flask, flask-cors, flask-socketio, pyyaml, rospkg, py_trees

Une fois les dépendances installées l'application se lance via la commande `python3 flaskr/run.py` et tourne sur le `localhost:5000`.

:warning: Pour le lancement `roscore` et `moveit` doivent être en cours d'exécution

## :book: Documentation

| URL          | Method | Body | Return Code     |    Return          |      Description            |
|:-------------|:--------| :--- | :---- |:-----|:---------------------------------|
| /            | GET     | | 200  | {"Success": "Server is running"} |                        |
| /robot_state | GET     | | 200  | {'robot_state': True}            |                        |
| /robot_state | GET     | | 404  |                                  | Robot is not alive     |
| /shutdown    | GET     | |      |                                  | Shutdown flask server  |
| /free/       | GET     | | 200  | {'compliant': 'True'}            | Robot is compliant     |
| /free/       | GET     | | 200  | {'compliant': 'False'}           | Robot is not compliant |
| /free/       | POST    |{'compliant': 'True'}     | 200  | {'compliant': 'True'}       | Robot has been set compliant |
| /free/       | POST    |{'compliant': 'False'}     | 200  | {'compliant': 'False'}       | Robot has been set not compliant |
| /free/       | POST    |None or incorrect    | 400  | Bad Request      ||
| /free/       | POST    | {'compliant' : 'Bool'}    | 404  | Not Found       | Robot is not alive |
| /point/add/rviz | POST | {} | 408 | {"Error": "Rviz doesn't send response"} | Rviz is not alive or very slow |
| /point/add/rviz | POST | {} | 200 | {"Success" : "Add cartesian point with id: int"} | A point has been recorded |
| /point/add/free | POST | {} | 408 | {"Error": "MoveIt doesn't send response"} | MoveIt is not alive or very slow |
| /point/add/free | POST | {} | 200 | {"Success" : "Add cartesian point with id: int"} | A point has been recorded |
| /point/get | GET | | 404 | {"Error": "No point have been recorded"} | ros parameters server (on the name "cartesianPoints") is empty  |
| /point/get | GET | | 200 | A json with all cartesian points | |
| /point/get/<id> | GET | | 404 | {"Error": "No point have been recorded"} |ros parameters server (on the name "cartesianPoints") doesn't contain point with this id |
| /point/get/<id> | GET | | 200 | A json with one point | |
| /point/delete | POST | {} | 200 | {"Success": "All points have been deleted"} | All points have been cleared or database was empty |
| /point/delete/<id> | POST | {} | 404 | {"Error": "No point match with id: int" | ros parameters server (on the name "cartesianPoints") doesn't contain point with this id  |
| /point/delete/<id> | POST | {} | 200 | {"Success": "Point have been deleted"} | Point has been deleted |
| /control/ | POST | an export of nodered tree | 200 | {"Success": "All behavior trees has been executed"} | |
| /control/ | POST | None | 400 | {"Error": "json is empty"} | Can't evaluate an empty file |
| /control/ | POST | an export of nodered tree| 400 | {"Error": "json contains 0 valid roots"} | Json is not empty but doesn't contain root block |
| /control/ | POST | an export of nodered tree| 400 | {"Error": "Tree with root id <id> is incorrect"} | Json contains a root block but associate tree is incorrect|
| /control/ | POST | an export of nodered tree| 400 | {"Error": "Block (or child of this block) with id <id> is incorrect"} | Json contains contains tree but one block is incorrect|
| /control/stop | GET | | 200 | {"Success": "Behavior tree has been stopped "} | Current behavior tree is stopped|


