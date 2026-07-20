const storeKey='fde-agri-learning-v1';
const defaultState={tasks:{},practice:{},hours:0,review:{learned:'',built:'',errors:'',adjust:''}};
let state=JSON.parse(localStorage.getItem(storeKey)||'null')||defaultState;

const todayTasks=[['t1','确认Python、VS Code和Git可以运行','60分钟'],['t2','观看变量、数据类型和输入输出章节','50分钟'],['t3','跟写亩数换算和产量计算程序','60分钟'],['t4','独立完成day1_farm_profile.py','60分钟'],['t5','测试正常值、0、负数和文字输入','30分钟'],['t6','记录一个报错和今天复盘','30分钟']];
const weeks=[
['第1周','Python · Git · API','命令行成本计算器与第一次AI调用','能处理异常；至少5次Git提交；可解释70%代码'],
['第2周','Streamlit · 文件检索','可上传资料并显示引用的本地网页','资料不足时拒答；15条检索问题'],
['第3周','Function Calling','成本工具与结构化农事计划','关键数字由代码计算；结果字段固定'],
['第4周','FastAPI · SQL · Evals','接口、历史记录与30条测试集','成本测试100%；高风险建议人工复核'],
['第5周','Docker · 部署 · 日志','互联网可访问的测试版','密钥不入库；重启恢复；日志可查'],
['第6周','用户试用 · 作品集','2名用户反馈与5分钟演示','讲清问题、方案、结果、限制']];
const days=[
['第1天','环境、变量与输入输出','农场概况程序','day1_farm_profile.py'],['第2天','判断、循环、列表与字典','成本计算器V1','day2_cost_calculator.py'],['第3天','函数、模块与异常','成本计算器V2','day3_cost_calculator_v2.py'],['第4天','文件、CSV与JSON','文件驱动成本计算','inputs.csv + result.json'],['第5天','Git、调试与测试','5组自动测试','test_cost_calculator.py'],['第6天','HTTP、API与环境变量','第一次模型调用','day6_first_ai_call.py'],['第7天','整合、演示与复盘','命令行AI原型','week1_cli_prototype.py']];
const practices=[
['01','农场概况','变量、输入、数字转换和输出'],['02','亩产是否达标','if/elif/else与边界条件'],['03','农资成本累计','列表、字典和for循环'],['04','成本函数拆分','参数、返回值与职责分离'],['05','无效输入处理','try/except和错误提示'],['06','CSV到JSON','文件读写、字段校验和编码'],['07','成本计算测试','正常、0、负数、小数、空数据'],['08','第一次API调用','HTTP、JSON、环境变量和SDK']];
const resources=[
['中文视频·必看','北京理工大学Python语言程序设计','第1周按需观看快速入门到文件章节','https://www.icourse163.org/course/BIT-268001?tid=317001'],
['中文视频·补充','黑马程序员Python零基础教程','卡住时补看对应章节，不连续刷课','https://www.bilibili.com/video/BV1qW4y1a7fU/'],
['官方文档','Python中文教程','查语法和示例，不要求通读','https://docs.python.org/zh-cn/3/tutorial/'],
['官方文档','GitHub中文入门','完成仓库、提交和历史查看','https://docs.github.com/zh/get-started/onboarding/getting-started-with-your-github-account'],
['官方文档','OpenAI开发者快速入门','第6天完成第一次Responses API调用','https://developers.openai.com/api/docs/quickstart'],
['官方教程','Streamlit Get Started','第2周构建网页','https://docs.streamlit.io/get-started'],
['官方文档','File Search','第2周构建带引用的资料问答','https://developers.openai.com/api/docs/guides/tools-file-search'],
['官方文档','Function Calling','第3周让模型调用成本工具','https://developers.openai.com/api/docs/guides/function-calling'],
['官方中文','FastAPI','第4周构建后端接口','https://fastapi.tiangolo.com/zh/'],
['官方视频','OpenAI Academy Evals','第4周理解生产级AI评测','https://academy.openai.com/public/videos/evals-the-key-to-production-ready-ai-apps-2025-06-24']];

function save(){localStorage.setItem(storeKey,JSON.stringify(state));renderMetrics()}
function renderTasks(){const el=document.querySelector('#today-tasks');el.innerHTML=todayTasks.map(([id,label,time])=>`<label class="task ${state.tasks[id]?'done':''}"><input type="checkbox" data-task="${id}" ${state.tasks[id]?'checked':''}><span>${label}</span><small>${time}</small></label>`).join('');el.querySelectorAll('input').forEach(i=>i.addEventListener('change',e=>{state.tasks[e.target.dataset.task]=e.target.checked;save();renderTasks()}))}
function renderMetrics(){const taskDone=Object.values(state.tasks).filter(Boolean).length;const practiceDone=Object.values(state.practice).filter(Boolean).length;const done=taskDone+practiceDone;const total=todayTasks.length+practices.length;const pct=Math.round(done/total*100);document.querySelector('#total-progress').textContent=pct+'%';document.querySelector('#progress-bar').style.width=pct+'%';document.querySelector('#done-count').textContent=`${done} / ${total}`;document.querySelector('#total-hours').textContent=state.hours||0;const dot=document.querySelector('#status-dot'),label=document.querySelector('#risk-label');if(pct>=80){dot.style.background='#216e4e';label.textContent='绿色：进度正常'}else if(pct>=50){dot.style.background='#d99421';label.textContent='黄色：需要补缺'}else{dot.style.background='#a63d3d';label.textContent='红色：先完成今日产出'}}
function renderStatic(){document.querySelector('#roadmap-list').innerHTML=weeks.map(w=>`<article><span class="tag">${w[0]}</span><div><h2>${w[1]}</h2><p>${w[2]}</p></div><div><p><strong>验收：</strong>${w[3]}</p></div></article>`).join('');document.querySelector('#week-days').innerHTML=days.map(d=>`<article class="day-card"><span class="tag">${d[0]}</span><h2>${d[1]}</h2><p>${d[2]}</p><p class="deliverable">产出：${d[3]}</p></article>`).join('');document.querySelector('#practice-list').innerHTML=practices.map((p,i)=>`<article class="practice-card"><span class="num">${p[0]}</span><div><h2>${p[1]}</h2><p>${p[2]}</p></div><input type="checkbox" data-practice="p${i}" ${state.practice['p'+i]?'checked':''} aria-label="完成${p[1]}"></article>`).join('');document.querySelectorAll('[data-practice]').forEach(i=>i.addEventListener('change',e=>{state.practice[e.target.dataset.practice]=e.target.checked;save()}));document.querySelector('#resource-list').innerHTML=resources.map(r=>`<article class="resource-card"><span class="tag">${r[0]}</span><div><h2>${r[1]}</h2><p>${r[2]}</p></div><a href="${r[3]}" target="_blank" rel="noreferrer">打开资源</a></article>`).join('')}
function initNav(){document.querySelectorAll('.nav-item').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.nav-item,.view').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.querySelector('#'+b.dataset.view).classList.add('active');document.querySelector('#view-title').textContent=b.textContent}))}
function initForm(){document.querySelector('#hours-input').value=state.hours||'';document.querySelector('#save-hours').onclick=()=>{state.hours=Number(document.querySelector('#hours-input').value)||0;save()};Object.keys(state.review).forEach(k=>document.querySelector('#'+k).value=state.review[k]);document.querySelector('#save-review').onclick=()=>{Object.keys(state.review).forEach(k=>state.review[k]=document.querySelector('#'+k).value);save()};document.querySelector('#reset-data').onclick=()=>{if(confirm('确认清空全部打卡、时长和复盘吗？')){state=JSON.parse(JSON.stringify(defaultState));save();location.reload()}}}
initNav();renderTasks();renderStatic();initForm();renderMetrics();

