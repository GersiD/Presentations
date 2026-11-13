Presentation for reinforcement learning from verifyable rewards.

For the purposes of this presentation, we assume that the introduction to reinforcement learning has been done already.

Flow of the presentation:
0. Explain the the bitter lesson of richard sutton
    - Not just that imbuing systems with human knowledge doesn't scale, but that the "right way" to do it is to allow
    the system to "search" or learn from self experience.
    - This is the entire thesis of RL, allow agents to learn from self experience.
1. History of RL
    - Td-gammon, deep blue, alpha go, alpha zero
    - The whole idea of RL is to allow agents to learn from self experience, and the history of RL is a testament to that
    - We hope that by learning from experience agents can beat humans at complex tasks, and the history of RL is a testament to that 
    - this is basically the bitter lesson
2. Introduce the key concepts of RL that in this talk I will be trying to convince the audiance of
    - Learn from experience
    - Instead of learning behaviour, learn *value* of behaviour (greyed out since we havent talked about it)
3. Value of behaviour
    - imagine you are a golf player
    - you start at the tee and you are 300 yards away from the hole
    - you have so many choices, club, angle, strength
    - trying to learn these actions directly is very hard, and as actions scale, it becomes intractable
    - KEY IDEA instead we learn value of a state and calculate what effect each action would have on the value of the
    next state
4. Introduce RLVR
    - start here figure 1.1 https://rlvrbook.com/chapters/01-introduction.html
    - Highlight the environment, state, action, reward, and policy concepts
    - Discuss the limitations of supervised learning
5. How might we do this with LLMS?
    - Work up to GRPO by analyzing multiple trajectories and learning from the reward signals
6. Limitations in RLVR
    - Reward hacking, reward shaping, and the problem of sparse rewards
    - Credit assignment problem
    - is rlvr really uncovering the bitter lesson? or is it just a new way to do supervised learning?
7. Open problems in RLVR
    - Elicitation or creation? Are llms trained to elicit mathematical expertise or we truely creating mathematical expertise?
    - Might RL cause models to learn unnecessary behaviours that happened to lead to a reward signal?
    - How far can RLVR extend into tasks with no verifyable answer?
