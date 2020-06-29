# Pomop_queue - Poor man Pomodoro Queue

[![Build Status](https://travis-ci.org/tung491/pomop_queue.svg?branch=master)](https://travis-ci.org/tung491/pomop_queue)

Simple CLI app for run a pomodoro with task queue. Inherit from [pomop](https://github.com/hvnsweeting/pomop)


## Install
---------
`pip install pomop-queue`

## Usage 
### queue
| queue list      | list all task in queue  |   |   |   |
|-----------------|-------------------------|---|---|---|
| queue size      | print the size of queue |   |   |   |
| queue add       | Add a task into queue   |   |   |   |
| modify-name     | Modify name of task     |   |   |   |
| modify-priority | Modify priority of task |   |   |   |

### pomop
pomop next-task to print the next default task

pomop to execute a default pomodoro in 25 minutes

#### Options
| -l LENGTH, --length LENGTH | Length of Pomodoro in minutes      |   |   |   |
|----------------------------|------------------------------------|---|---|---|
| -S, --nosound              | Turn off sound notification        |   |   |   |
| -B, --nobrowser            | Turn off browser-open notification |   |   |   |

## Author
Tung Son Do - <dosontung007@gmail.com>
