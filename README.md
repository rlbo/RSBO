# Exploration via Cost-Aware Subgoal Design

## What do we have
### Requirements
  
  * MOE
  * Replace the corresponding files with the files in folder ```moe```, and rerun ```moe/optimal_learning/cpp/CMakeLists.txt``` and ```moe/optimal_learning/cpp/CMakeCache.txt```.

### Algorithms
  * BESD
  * EI
  * LCB
  * HyperBand
  * MAML
  * Q-learning

## How to run the algorithms
#### run BESD
  ```bash
  (VIRT_ENV) $ python run_besd_REP.py miso_gw 0 0 gw10Two1
  ```
  This is the main file for running BESD. It requests 4 inputs:
  
  1) The environment: besd_gw, besd_ky, besd_it, besd_mc
  
  2) Which problem: 0
  
  3) Replication number: 0,1,2,...
  
  4) Problem name: 
     
     besd_gw: gw10Two2, gw20Three1.
     
     besd_ky: ky10One.
     
     besd_it: it10.
     
     besd_mc: mcf2.
  
#### EI / LCB
  ```bash
  (VIRT_ENV) $ python main_gpyopt.py gw10Two1 EI 0 0
  ```
  1) Problem name: gw10Two1, gw20Three1, ky10One, it10, mcf2
  
  2) Algorithm: EI, LCB
  
  3) Version: 0
  
  4) Replication_no: 0,1,2,... 

#### HyperBand
  ```bash
  (VIRT_ENV) $ python main_hb.py gw10Two1 0 0
  ```
  1) Problem name: gw10Two1, gw20Three1, ky10One, it10, mcf2
  
  2) Version: 0
  
  3) Replication_no: 0,1,2,... 
  
#### MAML
Go to folder maml-rl-pytorch, then run the following:
```bash
  (VIRT_ENV) $ python train.py --config configs/maml/gw10Two1.yaml --output-folder result_gw10Two1 --seed 0 --num-workers 8
  ```

#### Vanilla Q-learning
  ```bash
  (VIRT_ENV) $ python main_ql.py it10 0
  ```
  1) Problem name: gw10Two1, gw20Three1, ky10One, it10, mcf2
  
  2) Replication_no: 0,1,2,...
