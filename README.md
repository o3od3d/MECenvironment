# MECenvironment


- MEC envirionment을 위한 시뮬레이션으로 클라우드의 데이터 센터, MEC 서버, IIoT 장치로 총 3계층으로 환경을 구성하였다.
- task offloading을 수행하는 시뮬레이션으로 효율적인(Throughput, communication failure, regret, utility 측면에서) task offloading을 위해 Multi-Armed Bandit의 수정한 Discounted Thomson Sampling과 이중 경매이론의 MacAfee's 메커니즘을 적용하였다.
- 비교한 기법은 기존의 Discounted Thomson Sampling과 discountedUCB이다.
</br>
</br>

## FILE DESCRIPTION


- simulation_exe.py 
  - 해당 파일을 통해 시뮬레이션을 실행할 수 있으며, 실행 결과는 제안한 기법과 비교 기법의 Throughput, communication failure, regret, utility 그래프가 도출된다. 
  - 이 파일에서 생성할 기기 수와 총 라운드 횟수를 설정할 수 있다.


- IIoTdevice.py MEC 
  - 커버리지 내에 생성되는 IIoT 기기들을 생성하는 코드로 이 코드에서 각 IIoT 기기의 위치별로 상세하게 D2D task offloading을 위한 클러스터링 작업이 수행된다.


- MECServer.py 
  - MEC서버도 task를 처리하기 때문에 이 코드를 통해 MEC 서버가 태스크를 처리하게 된다.


- task.py 
  - 각 IIoT 기기별로 태스크를 생성하는데, 각 태스크는 gernerateTime과 computation capacity, datasize, bid, energy, taskstatus,tolerancelatency로 구성되어 생성된다.
  - taststatus는 처리완료, 태스크 취소(tolerancelatency 넘을 경우), 태스크 처리 대기 로 구성된다.


- proposed_DTS.py 
  - 논문에서 제안한 Multi-Armed Bandit의 Discounted Thomson Sampling 코드이다.


- proposed_double_auction.py 
  - 논문에서 제안한 기법에 사용된 double auction의 McAfee's Mechanism이다.


- existing_DTS.py 
  - 제안한 기법과 비교할 기존의 Multi-Armed Bandit의 Discounted Thomson Sampling 코드이다.


- discountedUCB.py 
  - 제안할 기법과 비교할 기존의 Multi-Armed Bandit의 Discounted UCB(Upper Confidence Bound) 코드이다.
</br>
</br>

  
## SIMULATION RESULT

<div align="center">
  
### Throughput


![image](https://github.com/o3od3d/MECenvironment/assets/44185083/578586a5-5226-4c5a-af4a-537987d370b0)

### Communication failure


![image](https://github.com/o3od3d/MECenvironment/assets/44185083/0f597863-093e-4d3e-aad1-f8964dcfa6a9)

### Regret


![image](https://github.com/o3od3d/MECenvironment/assets/44185083/894214ed-85e4-46af-9dcf-c68ce938e297)

### Utility

  
![image](https://github.com/o3od3d/MECenvironment/assets/44185083/7f63ce92-580a-437f-9f13-afb1542c117a)



</div>

## papers


> **reference : https://github.com/jlggross/MEC-simulator
