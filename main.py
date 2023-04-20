import subprocess
import time

while True:
    process = subprocess.Popen(['nohup', 'python', 'checker.py' , '&'])
    while process.poll() is None:
        # Le processus est en cours d'exécution
        time.sleep(1)

    # Le processus s'est terminé, nous allons le relancer
    print('Le script a été arrêté, il sera relancé...')
