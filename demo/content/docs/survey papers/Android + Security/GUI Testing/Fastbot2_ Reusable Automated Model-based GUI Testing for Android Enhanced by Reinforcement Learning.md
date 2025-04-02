---
title: 'Fastbot2: Reusable Automated Model-based GUI Testing for Android Enhanced by Reinforcement Learning'
tags: [Meeting Paper]

---

# Fastbot2: Reusable Automated Model-based GUI Testing for Android Enhanced by Reinforcement Learning
:::info
Lv, Z., Peng, C., Zhang, Z., Su, T., Liu, K., & Yang, P. (2022, October). Fastbot2: Reusable automated model-based gui testing for android enhanced by reinforcement learning. In Proceedings of the 37th IEEE/ACM International Conference on Automated Software Engineering (pp. 1-5).
:::
參考資料: https://github.com/bytedance/Fastbot_Android/blob/main/handbook-cn.md
![image](https://hackmd.io/_uploads/SJFpdcp51x.png)

## 動機與貢獻
現有的GUI testing都是無法重複使用之前測試的結果，但fastbot2可以(特別是event-activity transitions)。有兩個貢獻
1. 提出reusable automated model-based GUI testing technique，並且利用reinforcement learning進行增強，以滿足持續測試的實際需求
2. Fastbot2 優於最先進的技術。它也已成功部署在位元組跳動的 CI 流程中，並因其改善應用程式品質的能力而獲得了積極的回饋
## 主要流程
1. 其實很簡單，就是2個東西合併，一個是可以儲存過往測試的流程中，event和activity之間的關係(transitions)，該機率模型就是在記憶每一次的測試round中，獲得的一些knowledge，比方說哪一個哪些event會跑到哪個activity之類的；
> 旨在根據曾經探索的頁面的情況，對當前的備選組件進行挑選，從中選出最有可能觸發未曾探索過的頁面的組件，也就更有可能提升測試結果的 Activity 覆蓋率

另一個就是決定如何event的RL agent
3. a1~a3: 擷取apk檔案中的valid text(static text labels widgets)；接著安裝在手機上，如果之前有測試過就把相關紀錄以及儲存的東西提取出來給機率模型
4. b1~b6: 首先把目前的GUI畫面傳給hyper-event abstractor，這樣就會知道目前畫面有哪些event可以觸發，接著藉由機率模型以及RL agent選擇一個event，並且實際執行，最後把下一個畫面的資訊同步更新給機率模型以及historical data中，重複b1~b6的步驟直到時間結束

如以下這個示意圖，當頭條這個App被initial trigger之後，按了e1這個event會跑到activity 2，而按了e2和e5這2個events，都會跑到activity 3
![image](https://hackmd.io/_uploads/SJ4a0qa5ke.png)
因此，作者就給出了下面的機率模型，觸發e2和e4，會100%的跑到activity 3和activity 1
![image](https://hackmd.io/_uploads/S1U4ys6ckl.png)
> 具體來說，對於當前一個潛在可以交互的組件 e，Fastbot 會根據之前探索的情況讀取這個組件 e 曾經可以觸發的 Activity，並將目前本輪探索到的 Activity 與歷史數據進行對比。如果目前 Fastbot 並沒有觸發到組件 e 中曾經觸發過的部分 Activity，並且相較於當前頁面的其他組件來說，此組件 e 仍未被觸發的 Activity 數量最多，那麽此組件 e 就會被概率模型選中。如下圖所示，概率模型會計算每一個 e 的概率，E(e) 代表此組件 e 之前所觸發的 Activity 中未在本輪中被觸發的比例。
>![formula1](https://hackmd.io/_uploads/BJYcZjTqJx.png)
> 需要說明的是，此概率模型會在 Fastbot 的過程中隨時保存，並且也會在下一次測試的時候被使用。這也是此模型被稱為概率模型的原因，因為它記錄了應用的歷史探索的情況。
> 如果此應用從未被測試過，也並未儲存過概率模型，那麽 Fastbot 會以隨機選擇組件的方式應對冷啟動的問題。

### 
## Code Analysis
可以直接看官方的說明: https://github.com/bytedance/Fastbot_Android/blob/main/fastbot_code_analysis.md
總之如果想要研究具體決策的model，要看Native Folder(c++)，如果想要知道native怎麼和mobile溝通，要看mokey folder(java)
我是只有看native，要具體來看他怎麼進行決策。
從上到下的順序如下
* native/project/jni/fastbot_native.cpp # 該文件為上層的Java層提供了JNI的介面實作。其中 b0bhkadf函數提供了決策的核心功能。 
    ```cpp=28
        std::string operationString = _fastbot_model->getOperate(xmlString, activityString);
    ```
* native/model/Model.cpp
    ```cpp=74
    std::string Model::getOperate(const ElementPtr &element, const std::string &activity,
                                      const std::string &deviceID) {
            OperatePtr operate = getOperateOpt(element, activity, deviceID);
            std::string operateString = operate->toString(); // wrap the operation as a json object and get its string
            return operateString;
        }


        OperatePtr Model::getOperateOpt(const ElementPtr &element, const std::string &activity,
                                        const std::string &deviceID) {
        ...
        action = std::dynamic_pointer_cast<Action>(agent->resolveNewAction());
        agent->updateStrategy();
    ```
    這裡有兩個主要的操作，一個是#85選出一個action送到java layer執行，另外一個是要update agent，以下先列出如何選出action
* native/agent/AbstractAgent.cpp
    ```cpp=105
        ActionPtr AbstractAgent::resolveNewAction() {
            // update priority
            this->adjustActions();
            ActionPtr action = this->selectNewAction();
            _newAction = std::dynamic_pointer_cast<ActivityStateAction>(action);
            return action;
        }
    ```
* native/agent/ModelReusableAgent.cpp: 這是最重要的核心，也就是決定了如何判斷要哪一個action(就是hyper-event)要被執行
    ```cpp=248
        ActionPtr ModelReusableAgent::selectNewAction() {
            ActionPtr action = nullptr;
            action = this->selectUnperformedActionNotInReuseModel();
            if (nullptr != action) {
                BLOG("%s", "select action not in reuse model");
                return action;
            }

            action = this->selectUnperformedActionInReuseModel();
            if (nullptr != action) {
                BLOG("%s", "select action in reuse model");
                return action;
            }

            action = this->_newState->randomPickUnvisitedAction();
            if (nullptr != action) {
                BLOG("%s", "select action in unvisited action");
                return action;
            }

            // if all the actions are explored, use those two methods to generate new action based on q value.
            // there are two methods to choose from.
            // based on q value and a uniform distribution, select an action with the highest value.
            action = this->selectActionByQValue();
            if (nullptr != action) {
                BLOG("%s", "select action by qvalue");
                return action;
            }

            // use the traditional epsilon greedy strategy to choose the next action.
            action = this->selectNewActionEpsilonGreedyRandomly();
            if (nullptr != action) {
                BLOG("%s", "select action by EpsilonGreedyRandom");
                return action;
            }
            BLOGE("null action happened , handle null action");
            return handleNullAction();
        }
    ```
* native/agent/ModelReusableAgent.cpp: 這一段開始就是說明如何update agent，包含用在論文中提到的那些sarsa formula更新q-value等等
    ```cpp=169
        void ModelReusableAgent::updateStrategy() {
            if (nullptr == this->_newAction) // need to call resolveNewAction to update _newAction
                return;
            // _previousActions is a vector storing certain amount of actions, of which length equals to SarsaNStep.
            if (!this->_previousActions.empty()) {
                this->computeRewardOfLatestAction();
                this->updateReuseModel();
                double value = getQValue(_newAction);
                for (int i = static_cast<int>(this->_previousActions.size()) - 1; i >= 0; i--) {
                    double currentQValue = getQValue(_previousActions[i]);
                    double currentRewardValue = this->_rewardCache[i];
                    // accumulated reward from the newest actions
                    value = currentRewardValue + SarsaRLDefaultGamma * value;
                    // Should not update the q value during step (action edge) between i+1 to i+n-1
                    // The following statement is slightly different from the original sarsa RL paper.
                    // Considering to move the next statement outside of this block.
                    // Since only the oldest action should be updated.
                    if (i == 0)
                        setQValue(this->_previousActions[i],
                                  currentQValue + this->_alpha * (value - currentQValue));
                }
            } else {
                BDLOG("%s", "get action value failed!");
            }
            // add the new action to the back of the cache.
            this->_previousActions.emplace_back(this->_newAction);
            if (this->_previousActions.size() > SarsaNStep) {
                // if the cached length is over SarsaNStep, erase the first action from cache.
                this->_previousActions.erase(this->_previousActions.begin());
            }
        }
    
## code和論文中的公式對應
以下function都在native/agent/ModelReusableAgent.cpp/中
* Equ.1: probabilityOfVisitingNewActivities()
    $P(e,A_i)=\frac{N(e,A_i)}{N(e)}$
* Equ.2: selectUnperformedActionInReuseModel()
    $P_M(e_i)=exp({\mathbb{E}(e_i)\over\alpha})/\sum_{e_i\in\mathcal{E}_c}exp({\mathbb{E}(e_i)\over\alpha})$
* Equ.3: updateStrategy()
    $Q(e_t)+\alpha(G_{t,t+n}-Q(e_t))$
    $G_{t,t+n}=r_{t+1}+\gamma r_{t+2}+\dots+\gamma^n Q(e_{t+n})$
* Equ.4: computeRewardOfLatestAction()
    $r_{t+1}={\mathbb{E}(e_t)\over\sqrt{N(e_t)+1}}+{V\over\sqrt{N(A_t)+1}}$
* Equ.5: getStateActionExpectationValue()
    $V=n_h+0.5*n_c+\sum_{e_i\in\mathcal{E}_c}\mathbb{E}(e_i)$
* Equ.6: selectActionByQValue()
    $P_Q(e_i)=exp({{Q(e_i)\over\beta}})/{\sum_{e_i\in\mathcal{E}_c}exp({Q(e_i)\over\beta})}$
* Inline Equation: probabilityOfVisitingNewActivities()
    $\mathbb{E}(e_i)=\sum_{A\notin\mathcal{A}_t}P(e_i,A),0\le i\le |\mathcal{E}_c|$