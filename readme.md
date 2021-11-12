# Simple Reinforcement Learning with AI snake

## 💼 Technical Skills

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
 ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
 
## 📈 GitHub Stats 

[![Sang's github stats](https://github-readme-stats.vercel.app/api?username=sangngoc27042001)](https://github.com/sangngoc27042001)

[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=yushi1007&layout=compact)](https://github.com/sangngoc27042001)

[![Visitors](https://visitor-badge.glitch.me/badge?page_id=yushi1007.yushi1007)](https://www.yushi.dev/)

## 🤝 Connect with me:

<a href="https://www.facebook.com/sang.vongoc.3532/"><img align="left" src="https://github.com/sangngoc27042001/Dummy-files/blob/main/facebook.png" alt="Sang Vo | Facebook" width="21px"/></a>
<a href="https://www.instagram.com/sangvongoc/"><img align="left" src="https://github.com/sangngoc27042001/Dummy-files/blob/main/instagram.png" alt="Sang Vo | Instagram" width="21px"/></a>
<a href="sangngoc27042001@gmail.com"><img align="left" src="https://github.com/sangngoc27042001/Dummy-files/blob/main/gmail.png" alt="Sang Vo | Gmail" width="21px"/></a>
</br>

## Instruction
- You can play the snake game normally by running the file **pure_snake_game.py**.
- First, you have to run the **generate_first_model.py** to generate an untrained model.
```
python generate_first_model.py
```
- Then, you can run the **snake.py** to see how our snake make progress through several games.
```
python snake.py
```
-  About the file **snake.py**, the variable **WIDTH** is changable. This variable will determine the size of snake's play ground (it must be divisible by 2).
-  This is an example of an AI snake.
 <br>![Alt text](/images/master.gif "a title")<br>
## About the technique
### 1. State
- The state will contain the information of current dirrection of the snake, food and dangers surrounding it.
- The state array will have 11 elements. The first 3 is used for detecting the dangers, the next four states for the snake's directions, and the final 4 states for the direction of food according to the snake's head.
- Let's consider this bellow example.<br>
![Alt text](/images/state_1.png "a title")<br>
Because there is no dangers surrounding the snake's head, so the first 3 is all 0. As the current direction is to the right, so we get ```[0,1,0,0]``` in the next 4 elements. The fodd is upper and on the right side of the snake, so we get  ```[0,1,1,0]``` in the final 4.
```python
[
    0,0,0,  #straight, left, right
    1,0,0,0 #left, right, up, down
    0,1,1,0 #left, right, up, down
]
```
- Let's consider another example.<br>
![Alt text](/images/state_2.png "a title")<br>
Because there is dangerous if the snake turns left, so we get ```[0,1,0]``` in the first 3.
```python
[
    0,1,0,  #straight, left, right
    1,0,0,0 #left, right, up, down
    1,0,1,0 #left, right, up, down
]
```
### 2. Neural network
- The neural network will take in an array of 11 elements as input, and then generate an aray of size 3 as output, the element having the highest score will be selected as the final dicision of the next move.
<br>![Alt text](/images/neural_net_img.png "a title")<br>
## Evaluate the snake
- These line charts bellow will illustrate the progress that the snake have made through several games.
- Setting size of the play ground as 6x6 blocks
<br>![Alt text](/images/1.jpg "a title")<br>
- Setting size of the play ground as 8x8 blocks
<br>![Alt text](/images/2.jpg "a title")<br>
- Snake movement at some initial games.
<br>![Alt text](/images/bad.gif "a title")<br>
- Snake movement after several games.
<br>![Alt text](/images/good.gif "a title")<br>
