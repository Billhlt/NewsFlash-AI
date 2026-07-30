<template>
  <div class="bg-overlay"></div>
  <div class="container">
   <div class="wrapper">
    <!-- 重要文章内容 -->
    <div
      v-for="i in div_count"
      :key="i"
      class="box"
      :class="{ 'selected': selectedBoxes.includes(i-1) }"
    >
      <div class="text-content" v-html="processedTexts[i-1]" @mouseover="showTooltip" @mouseout="hideTooltip"></div>
       <div class="button-container">
         <button class="border-toggle" @click="toggleBoxBorder(i-1)">边框</button>
         <!--openArticleLink(i-1)之所以是i-1，是因为v-for的索引是从1开始的，而数组索引是从0开始的。-->
         <button class="link-toggle" @click="openArticleLink(i-1)">链接</button>
       </div>
    </div>
  </div>
  <!-- 写入文件按钮 -->
  <div class="write-file-container">
    <button class="write-file-button" @click="writeSelectedTextsToFile">写入本地文件</button>
  </div>
    <!-- 三个并排显示的容器 -->
    <div class="three-boxes-wrapper">
      <!-- 不重要文章内容 -->
      <div class="box three-box">
        <div class="set2-container">
          <!-- v-for遍历数组时，index从0开始，所以不需要减1，如果遍历的是数字，则循环从1开始，需要减1 -->
          <div 
            v-for="(item, index) in set2" 
            :key="index" 
            class="set2-row"
          >
            <div 
              class="set2-text" 
              :class="{ 'highlight-effect': highlightedTexts.has(`set2-${index}`) }"
              :id="`set2-text-${index}`"
            >{{ item }}</div>
            <div class="button-group">
              <button class="set2-effect-button" @click="showTextEffect(index, 'set2')" title="显示特效"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="#500724" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></button>
              <button class="set2-button" @click="openArticleLink2(index)"></button>
            </div>
          </div>
          <!-- set2写入文件按钮 -->
          <div class="set2-write-file-container">
            <button class="set2-write-file-button" @click="writeSet2TextsToFile">写入本地文件</button>
          </div>
        </div>
      </div>

      <!-- github项目列表 -->
      <div class="box three-box">
        <div class="set3-container">
          <div 
            v-for="(item, index) in set3" 
            :key="index" 
            class="set3-row"
          >
            <div 
              class="set3-text" 
              :class="{ 'highlight-effect': highlightedTexts.has(`set3-${index}`) }"
              :id="`set3-text-${index}`"
              v-html="item"
            ></div>
            <div class="button-group">
              <button class="set3-effect-button" @click="showTextEffect(index, 'set3')" title="显示特效"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="#500724" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></button>
              <button class="set3-button" @click="openArticleLink3(index)"></button>
            </div>
          </div>
          <!-- set3写入文件按钮 -->
          <div class="set3-write-file-container">
            <button class="set3-write-file-button" @click="writeSet3TextsToFile">写入本地文件</button>
          </div>
        </div>
      </div>

      <!-- producthunt项目列表 -->
      <div class="box three-box">
        <div class="set4-container">
          <div 
            v-for="(item, index) in set4" 
            :key="index" 
            class="set4-row"
          >
            <div 
              class="set4-text" 
              :class="{ 'highlight-effect': highlightedTexts.has(`set4-${index}`) }"
              :id="`set4-text-${index}`"
              v-html="item"
            ></div>
            <div class="button-group">
              <button class="set4-effect-button" @click="showTextEffect(index, 'set4')" title="显示特效"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="#500724" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></button>
              <button class="set4-button" @click="openArticleLink4(index)"></button>
            </div>
          </div>
          <!-- set4写入文件按钮 -->
          <div class="set4-write-file-container">
            <button class="set4-write-file-button" @click="writeSet4TextsToFile">写入本地文件</button>
          </div>
        </div>
      </div>
    </div>

  

  </div>

  <!-- 弹出文本框 -->
  <div v-if="tooltipVisible" class="tooltip" :style="tooltipStyle">
    {{ tooltipContent }}
  </div>
</template>

<script setup>
import { 
  chatAPI, 
  getSummary01, 
  getWordPosition01,
  getUrl01,
  getUrl02,
  getSummary02,
  getProducthunt,
  getProducthuntUrls,
  getGithub,
  getGithubName,
  writeTextsToFile,
  writeTextsToGithubFile,
  writeTextsToProducthuntFile
} from './services/api'
import { ref, computed, onMounted } from 'vue'


const div_count = ref(0)
const first = ref(null)
const userInput = ref('');
const messages = ref([]);
const valuez = ref([]);
const selectedBoxes = ref([]); // 跟踪被选中的box




//############################以下为测试用例################################
// const set1 = ref(['中国稀土8月1日股价下跌3.12%，成交额18.44亿元。中美经贸会谈达成延长暂停加征关税措施90天的协议，并就中国稀土出口进行细化谈判。中国在全球稀土及永磁材料市场占据主导地位，这使其在贸易谈判中具有重要筹码。当前舆情以正面为主，占比68.4%。贸易关系缓和、稀土出口协议细化以及中国稀土市场主导地位等因素短期内可能对稀土股价产生积极影响，长期则取决于中美贸易关系的持续稳定。主要传播渠道为今日头条平台。'   ,'午休的电梯里，我独自上升。镜面墙映出四个我，像被切片的时间。13层按钮亮着，像颗不肯熄灭的星。'   ,'清理外婆的旧冰箱时，我在冷冻室发现一只冻成琥珀的知了。它翅膀上的脉络，像被封存的银河地图。'   ,'末班地铁像条疲惫的龙，驮着零星乘客滑进隧道。我对面的男人抱着纸箱，箱里探出一只奶猫的脑袋，琥珀色眼睛盯着我。'   ,'凌晨三点，便利店像座发光的孤岛。我蹲在冰柜前挑酸奶，忽然听见收银台传来"生日快乐"的旋律——店员正对着一块小蛋糕，给自己点蜡烛。'   ,'凌晨两点，便利店的日光灯管嗡嗡作响。我蹲在冰柜前挑速食饭团，发现最里面藏着一个过期三天的金枪鱼口味。'   ,'末班地铁像条喝醉的银龙，在隧道里东倒西歪。我对面的西装男正用领带擦眼镜，镜片下是哭肿的眼皮。'   ,'梧桐把整条街拧出绿色的水。我躲进"昨日书屋"时，店主正在用毛笔给一本《昆虫记》画插图，钢笔画的蚂蚁背着米粒大的米开朗琪罗雕像。'   ,'整理外婆遗物时发现本1998年的日历，六月份以后全是空白，直到12月31日突然出现她歪歪扭扭的字："今天小孙子说我的皱纹像葡萄干。'   ,'批发市场的灯管冻成青白色，番茄堆成火山，辣椒在编织袋里流血。戴雷锋帽的老汉把最后一把菠菜塞进我篮子："姑娘，这菜今早三点还在地里做梦。'   ,'大厦停电时，我和一个穿恐龙睡衣的男孩被困在17楼。他用手机光照亮电梯广告，突然指着某理财产品的秃头经理说："这是我爸。"', '123hahahahahah大厦停电时，我和一个穿恐龙睡衣的男孩被困在17楼。他用手机光照亮电梯广告，突然指着某理财产品的秃头经理说："这是我爸。"'])

// // 三维集合，表示要添加提示的字符位置（左闭右开区间），例：第一二个字的位置是[0, 2]，第四五个字的位置是[3, 5]
// const ranges = ref([[[12, 18], [3, 5], [10, 11]], [[1, 3], [4, 6], [11, 13]], [[2, 4], [5, 7], [12, 14]], [[3, 5], [6, 8], [13, 15]], [[4, 6], [7, 9], [14, 16]], [[5, 7], [8, 10], [15, 17]], [[6, 8], [9, 11], [16, 18]], [[7, 9], [10, 12], [17, 19]], [[8, 10], [11, 13], [18, 20]], [[9, 11], [12, 14], [19, 21]], [[10, 12], [13, 15], [20, 22]], [[11, 13], [14, 16], [20, 22]]]);

// // 添加提示信息数组
// const tooltipMessages = ref([['地铁末班车777', '雨天的旧书店77', '外婆的日历123'], ['地铁末班车778', '雨天的旧书店78', '外婆的日历124'], ['地铁末班车779', '雨天的旧书店79', '外婆的日历125'], ['地铁末班车780', '雨天的旧书店80', '外婆的日历126'], ['地铁末班车781', '雨天的旧书店81', '外婆的日历127'], ['地铁末班车782', '雨天的旧书店82', '外婆的日历128'], ['地铁末班车783', '雨天的旧书店83', '外婆的日历129'], ['地铁末班车784', '雨天的旧书店84', '外婆的日历130'], ['地铁末班车785', '雨天的旧书店85', '外婆的日历131'], ['地铁末班车786', '雨天的旧书店86', '外婆的日历132'], ['地铁末班车787', '雨天的旧书店87', '外婆的日历133'], ['地铁末班车779', '雨天的旧书店79', '外婆的日历125']]);
const set1 = ref([]);   // 总结内容 列表
const set2 = ref([]);   // 不重要文章内容 列表
const set3 = ref([]);   // github文章内容 列表
const set4 = ref([]);   // producthunt文章内容 列表
const url1 = ref([]);   // 重要文章链接 列表
const url2 = ref([]);   // 非重要文章链接 列表
const url3 = ref([]);   // github项目名链接 列表
const url4 = ref([]);   // producthunt文章链接 列表
const ranges = ref([]); // 需解释词语位置 列表
const tooltipMessages = ref([]); // 词语解释 列表
onMounted(async () => {
  try {
    const wordPositionResponse = await getWordPosition01();
    // 将ranges中的所有数字减去3
    ranges.value = wordPositionResponse.data.map(textRanges => 
      textRanges.map(range => 
        range.map(num => num - 3)
      )
    );
    
    const summaryResponse = await getSummary01();
    set1.value = summaryResponse.data;
    div_count.value = set1.value.length;  // 添加这行来更新div_count
    
    // 获取重要文章链接
    const url1Response = await getUrl01();
    url1.value = url1Response.data;
    
    // 获取非重要文章链接
    const url2Response = await getUrl02();
    url2.value = url2Response.data;
    
    // 获取不重要文章内容
    const summary02Response = await getSummary02();
    set2.value = summary02Response.data;
    
    // 获取producthunt文章内容
    const producthuntResponse = await getProducthunt();
    set4.value = producthuntResponse.data;
    
    // 获取producthunt文章链接
    const producthuntUrlsResponse = await getProducthuntUrls();
    url4.value = producthuntUrlsResponse.data;
    
    // 获取github文章内容
    const githubResponse = await getGithub();
    set3.value = githubResponse.data;
    
    // 获取github项目链接
    const githubNameResponse = await getGithubName();
    url3.value = githubNameResponse.data.map(name => `https://github.com/${name}`);
    
  } catch (error) {
    console.error('获取数据失败:', error);
  }
}
);






// 工具提示相关
const tooltipVisible = ref(false);
const tooltipContent = ref('');
const tooltipStyle = ref({
  position: 'absolute',
  zIndex: 1000,
  backgroundColor: '#333',
  color: '#fff',
  padding: '5px 10px',
  borderRadius: '4px',
  fontSize: '14px',
  maxWidth: '200px',
  wordWrap: 'break-word'
});

// 使用 computed 处理文本，动态添加 span 标签
const processedTexts = computed(() => {
  const result = [];
  
  // 为每个文本创建处理后的版本
  for (let textIndex = 0; textIndex < div_count.value; textIndex++) {
    const text = set1.value[textIndex]; // 使用对应的文本
    if (!text) {
      result.push('');
      continue;
    }
    
    let processed = '';
    let lastIndex = 0;
    
    // 获取当前文本的 ranges
    const currentRanges = ranges.value[textIndex] || [];
    // 对 ranges 进行排序，确保处理顺序正确
    const sortedRanges = [...currentRanges].sort((a, b) => a[0] - b[0]);
    
    for (let i = 0; i < sortedRanges.length; i++) {
      const [start, end] = sortedRanges[i];
      if (start >= text.length) continue; // 超出文本长度则跳过
      
      // 添加未处理的普通文本
      processed += text.slice(lastIndex, start);
      
      // 添加带提示的 span 标签
      const sliceText = text.slice(start, Math.min(end, text.length));
      // 使用对应的提示信息
      const tooltipMessage = tooltipMessages.value[textIndex] && tooltipMessages.value[textIndex][i] ? tooltipMessages.value[textIndex][i] : '默认提示信息';
      processed += `<span class="underlined-text" data-tooltip="${tooltipMessage}">${sliceText}</span>`;
      
      lastIndex = Math.min(end, text.length);
    }
    
    // 添加剩余文本
    processed += text.slice(lastIndex);
    
    result.push(processed);
  }
  
  return result;
});

// 显示工具提示
const showTooltip = (event) => {
  const target = event.target;
  if (target.classList.contains('underlined-text')) {
    tooltipContent.value = target.getAttribute('data-tooltip');
    tooltipVisible.value = true;

    // 计算工具提示的位置，确保不会超出屏幕
    const rect = target.getBoundingClientRect();
    let left = rect.left;
    let top = rect.bottom + 5; // 在元素下方显示，间隔5px

    // 检查是否会超出右边界
    if (left + 200 > window.innerWidth) {
      left = window.innerWidth - 210; // 留出10px的边距
    }

    // 检查是否会超出下边界
    if (top + 100 > window.innerHeight) {
      top = rect.top - 105; // 在元素上方显示
    }

    tooltipStyle.value = {
      ...tooltipStyle.value,
      left: `${left}px`,
      top: `${top}px`
    };
  }
};

// 隐藏工具提示
const hideTooltip = () => {
  tooltipVisible.value = false;
};

// 定义一个异步函数sendMessage，用于发送消息
const sendMessage = async (ID) => {
  // 如果用户输入不为空
  if (userInput.value.trim() !== '') {
    // 调用chatAPI.sendMessage方法，发送消息，并传入用户输入和随机数
    const reader = await chatAPI.sendMessage(userInput.value, ID);
    // 清空用户输入
    userInput.value = '';
    // 调用displayMessage方法，显示消息
    displayMessage(reader);
  }
};

const displayMessage = async (reader) => {
  // 创建一个utf-8编码的解码器
  const decoder = new TextDecoder("utf-8");
  // 在messages数组中添加一个空字符串作为初始消息
  messages.value.push('');
  // 获取初始消息的索引
  const messageIndex = messages.value.length - 1;
  // 循环读取数据
  while (true) {
    // 读取数据
    const { done, value } = await reader.read();
    // 如果读取完毕，则跳出循环
    if (done) break;
    // 将读取的数据解码并追加到messages数组中的消息
    messages.value[messageIndex] += decoder.decode(value);
  }
};

// 切换box边框颜色
const toggleBoxBorder = (index) => {
  const boxIndex = selectedBoxes.value.indexOf(index);
  if (boxIndex === -1) {
    // 如果box未被选中，则添加到选中列表
    selectedBoxes.value.push(index);
  } else {
    // 如果box已被选中，则从选中列表中移除
    selectedBoxes.value.splice(boxIndex, 1);
  }
};

// 打开文章链接
const openArticleLink = (index) => {

  const match = url1.value[index];  // 获取重要文章链接
  if (match) {  // 如果链接存在，则在新窗口中打开链接
    // 在新窗口中打开链接
    window.open(match, "_blank");
  }
};

// 打开非重要文章链接
const openArticleLink2 = (index) => {
  const match = url2.value[index];  // 获取非重要文章链接
  if (match) {  // 如果链接存在，则在新窗口中打开链接
    // 在新窗口中打开链接
    window.open(match, "_blank");
  }
};

// 打开github项目链接
const openArticleLink3 = (index) => {
  const match = url3.value[index];  // 获取github项目链接
  if (match) {  // 如果链接存在，则在新窗口中打开链接
    // 在新窗口中打开链接
    window.open(match, "_blank");
  }
};

// 打开producthunt项目链接
const openArticleLink4 = (index) => {
  const match = url4.value[index];  // 获取producthunt项目链接
  if (match) {  // 如果链接存在，则在新窗口中打开链接
    // 在新窗口中打开链接
    window.open(match, "_blank");
  }
};

// 特效显示相关 - 使用 Set 来跟踪哪些文本被高亮
const highlightedTexts = ref(new Set());

// 显示文本特效 - 直接在文本上添加高亮标记效果
const showTextEffect = (index, type) => {
  const key = `${type}-${index}`;
  
  // 如果已经高亮，则移除高亮
  if (highlightedTexts.value.has(key)) {
    highlightedTexts.value.delete(key);
    return;
  }
  
  // 添加高亮
  highlightedTexts.value.add(key);
};

// 写入选中的文本到文件
const writeSelectedTextsToFile = async () => {
  if (selectedBoxes.value.length === 0) {
    alert('请先选择要写入的box（点击边框按钮）');
    return;
  }
  
  try {
    // 收集所有高亮box的文本（使用原始文本set1.value，不包含HTML标签）
    const textsToWrite = selectedBoxes.value
      .sort((a, b) => a - b) // 按索引排序
      .map(index => set1.value[index])
      .filter(text => text); // 过滤掉空文本
    
    if (textsToWrite.length === 0) {
      alert('没有可写入的文本内容');
      return;
    }
    
    // 调用API写入文件
    await writeTextsToFile(textsToWrite);
    alert(`成功将 ${textsToWrite.length} 条文本写入文件！`);
  } catch (error) {
    console.error('写入文件失败:', error);
    alert('写入文件失败，请检查后端服务是否正常运行');
  }
};

// 写入set2中高亮的文本到文件
const writeSet2TextsToFile = async () => {
  try {
    // 收集所有高亮的set2文本
    const textsToWrite = [];
    for (let index = 0; index < set2.value.length; index++) {
      const key = `set2-${index}`;
      if (highlightedTexts.value.has(key)) {
        const text = set2.value[index];
        if (text) {
          textsToWrite.push({ index, text });
        }
      }
    }
    
    // 按索引排序
    textsToWrite.sort((a, b) => a.index - b.index);
    
    if (textsToWrite.length === 0) {
      alert('请先选择要写入的文本（点击✨按钮高亮）');
      return;
    }
    
    // 提取纯文本数组
    const texts = textsToWrite.map(item => item.text);
    
    // 调用API写入文件
    await writeTextsToFile(texts);
    alert(`成功将 ${texts.length} 条文本写入文件！`);
  } catch (error) {
    console.error('写入文件失败:', error);
    alert('写入文件失败，请检查后端服务是否正常运行');
  }
};

// 写入set3中高亮的文本到文件
const writeSet3TextsToFile = async () => {
  try {
    // 收集所有高亮的set3文本
    const textsToWrite = [];
    for (let index = 0; index < set3.value.length; index++) {
      const key = `set3-${index}`;
      if (highlightedTexts.value.has(key)) {
        const text = set3.value[index];
        if (text) {
          textsToWrite.push({ index, text });
        }
      }
    }
    
    // 按索引排序
    textsToWrite.sort((a, b) => a.index - b.index);
    
    if (textsToWrite.length === 0) {
      alert('请先选择要写入的文本（点击✨按钮高亮）');
      return;
    }
    
    // 提取纯文本数组
    const texts = textsToWrite.map(item => item.text);
    
    // 调用API写入文件（github项目整理.txt）
    await writeTextsToGithubFile(texts);
    alert(`成功将 ${texts.length} 条文本写入文件！`);
  } catch (error) {
    console.error('写入文件失败:', error);
    alert('写入文件失败，请检查后端服务是否正常运行');
  }
};

// 写入set4中高亮的文本到文件
const writeSet4TextsToFile = async () => {
  try {
    // 收集所有高亮的set4文本
    const textsToWrite = [];
    for (let index = 0; index < set4.value.length; index++) {
      const key = `set4-${index}`;
      if (highlightedTexts.value.has(key)) {
        const text = set4.value[index];
        if (text) {
          textsToWrite.push({ index, text });
        }
      }
    }
    
    // 按索引排序
    textsToWrite.sort((a, b) => a.index - b.index);
    
    if (textsToWrite.length === 0) {
      alert('请先选择要写入的文本（点击✨按钮高亮）');
      return;
    }
    
    // 提取纯文本数组
    const texts = textsToWrite.map(item => item.text);
    
    // 调用API写入文件（producthunt产品整理.txt）
    await writeTextsToProducthuntFile(texts);
    alert(`成功将 ${texts.length} 条文本写入文件！`);
  } catch (error) {
    console.error('写入文件失败:', error);
    alert('写入文件失败，请检查后端服务是否正常运行');
  }
};
</script>

<style scoped>
html, body {
  overflow: hidden; /* Prevent body scroll, container handles scrolling */
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: "Inter", "Microsoft YaHei", "PingFang SC", sans-serif;
}

.bg-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  background: 
    radial-gradient(circle at 15% 50%, rgba(255, 183, 197, 0.08) 0%, transparent 25%), 
    radial-gradient(circle at 85% 30%, rgba(255, 158, 181, 0.08) 0%, transparent 25%);
  animation: pulseOverlay 15s ease-in-out infinite alternate;
}

@keyframes pulseOverlay {
  0% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
  100% { opacity: 0.5; transform: scale(1); }
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 100vh; /* 最小高度为视口高度 */
  width: 2400px; /* 设置为固定宽度 */
  background: transparent;
  position: absolute;
  top: 50px;
  right: 50px;
  left: 50px;
  padding-bottom: 50px; /* 底部留白 */
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 183, 197, 0.4) rgba(255, 255, 255, 0.05);
}

.container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 183, 197, 0.4);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 183, 197, 0.6);
}

.context-menu-area {
  width: 200px;
  height: 100px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
}

.wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 固定四列 */
  grid-auto-rows: 1fr;                   /* 每行高度一致 */
  gap: 50px 35px;                        /* 上下间隔50px，左右间隔35px */
  padding: 1rem;
  /* 让最后一行从左到右依次摆放，右侧留白 */
  justify-items: stretch;                /* 默认拉伸，保证格子宽度一致 */
  align-items: stretch;                  /* 保证格子高度一致 */
  height: 100%;
  box-sizing: border-box;
  overflow: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 183, 197, 0.4) rgba(255, 255, 255, 0.05);
}

.wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.wrapper::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.wrapper::-webkit-scrollbar-thumb {
  background-color: rgba(255, 183, 197, 0.4);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.wrapper::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 183, 197, 0.6);
}

.box {
  width: 100%;
  max-width: 100%;
  height: 300px;
  background: rgba(30, 30, 40, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: #e0e0e0;
  font-size: 1.2rem;
  padding: 25px 20px 15px 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: hidden; /* Changed from auto to hidden to manage scrollbar in content */
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  position: relative;
  box-sizing: border-box;
}

.box:hover {
  transform: translateY(-5px);
  background: rgba(40, 40, 55, 0.7);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 255, 255, 0.2);
}

.box::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 183, 197, 0.15) 0%, rgba(255, 255, 255, 0) 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 0;
  pointer-events: none;
}

.box::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ffb7c5 0%, #ff9eb5 100%);
  opacity: 0;
  transition: opacity 0.3s ease, transform 0.3s ease;
  transform: scaleX(0);
  transform-origin: left;
  border-radius: 20px 20px 0 0;
}

.box:hover::before {
  opacity: 1;
}

.box:hover::after {
  opacity: 1;
  transform: scaleX(1);
}

/* 当box被选中时的边框样式 text-content*/
.box.selected {
  background: rgba(45, 45, 65, 0.85);
  box-shadow: 0 0 25px rgba(255, 183, 197, 0.4), 0 10px 40px rgba(0, 0, 0, 0.4);
  transform: translateY(-5px) scale(1.01);
  border: 1px solid rgba(255, 183, 197, 0.6);
}

.box.selected::before {
  opacity: 1;
  background: radial-gradient(circle, rgba(255, 183, 197, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
}

.box.selected::after {
  opacity: 1;
  transform: scaleX(1);
  height: 5px;
  background: linear-gradient(90deg, #ffb7c5 0%, #ff9eb5 100%);
}

.box:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 10px 20px rgba(0, 0, 0, 0.3);
  transform: translateY(-5px);
  border-color: rgba(255, 255, 255, 0.2);
}

/* tall-box 高度设置 */
#tall-box {
  height: 1000px;
}

/* 三个并排显示的容器包装器 */
.three-boxes-wrapper {
  display: flex;
  flex-direction: row;
  gap: 30px;
  width: 100%;
  margin-left: 30px;
  margin-top: 50px;
  justify-content: flex-start;
}

/* 三个并排显示的box样式 */
.three-box {
  width: 750px !important;
  height: 1200px !important;
  flex-shrink: 0;
}

.box-tall {
  width: 100%;
  max-width: 100%;
  height: 1200px;
  background: rgba(30, 30, 40, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  color: #e0e0e0;
  font-size: 1.2rem;
  padding: 25px 20px 15px 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  position: relative;
  box-sizing: border-box;
}

.box-tall::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 183, 197, 0.15) 0%, rgba(255, 255, 255, 0) 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 0;
  pointer-events: none;
}

.box-tall::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ffb7c5 0%, #ff9eb5 100%);
  opacity: 0;
  transition: opacity 0.3s ease, transform 0.3s ease;
  transform: scaleX(0);
  transform-origin: left;
  border-radius: 20px 20px 0 0;
}

.box-tall:hover::before {
  opacity: 1;
}

.box-tall:hover::after {
  opacity: 1;
  transform: scaleX(1);
}

.box-tall:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 10px 20px rgba(0, 0, 0, 0.3);
  transform: translateY(-5px);
  border-color: rgba(255, 255, 255, 0.2);
}

.text-content {
  width: 100%;
  text-align: justify;
  text-justify: inter-ideograph;
  line-height: 1.7;
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow-y: auto;
  flex-grow: 1;
  min-height: 200px;
  max-height: calc(100% - 95px);
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 183, 197, 0.4) rgba(255, 255, 255, 0.05);
  font-weight: 400;
  letter-spacing: 0.5px;
  position: relative;
  z-index: 1;
  color: #e0e0e0;
}

.text-content::-webkit-scrollbar {
  width: 4px;
}

.text-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin: 10px 0;
}

.text-content::-webkit-scrollbar-thumb {
  background-color: rgba(255, 183, 197, 0.4);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.text-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 183, 197, 0.6);
}

/* 使用深度选择器，样式会穿透到子组件 */
:deep(.underlined-text) {
  text-decoration: none;
  cursor: pointer;
  position: relative;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  padding-bottom: 2px;
  font-weight: 500;
  color: #ffd1dc;
}

:deep(.underlined-text)::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #ffb7c5 0%, #ff9eb5 100%);
  transition: width 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: 1px;
}

:deep(.underlined-text:hover) {
  color: #ffb7c5;
}

:deep(.underlined-text:hover)::after {
  width: 100%;
}

:deep(.tooltip) {
  position: fixed;
  z-index: 1000;
  background: rgba(30, 41, 59, 0.95);
  color: #ffffff;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  max-width: 250px;
  word-wrap: break-word;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25), 0 2px 10px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  animation: tooltipFadeIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transform-origin: center;
}

:deep(.tooltip)::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ffb7c5 0%, #ff9eb5 100%);
  border-radius: 12px 12px 0 0;
}

@keyframes tooltipFadeIn {
  from { 
    opacity: 0; 
    transform: translateY(15px) scale(0.9); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
}

/* 边框切换按钮样式 */
.border-toggle, .link-toggle {
  width: 50px;
  height: 50px;
  padding: 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.border-toggle:hover, .link-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(255, 183, 197, 0.4), 0 5px 15px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.border-toggle::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff9eb5 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}

.border-toggle::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 1;
}

.border-toggle span {
  position: relative;
  z-index: 2;
}



.border-toggle:hover::before {
  opacity: 1;
}

.border-toggle:hover::after {
  width: 100px;
  height: 100px;
}

.button-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 10px;
  /* 固定按钮容器高度，防止占用过多空间 */
  height: 50px;
  /* 防止按钮容器滚动 */
  flex-shrink: 0;
  margin-top: 10px;
}

/* content replaced by merged block above */

.link-toggle::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff9eb5 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}

.link-toggle::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 1;
}

.link-toggle span {
  position: relative;
  z-index: 2;
}



.link-toggle:hover::before {
  opacity: 1;
}

.link-toggle:hover::after {
  width: 100px;
  height: 100px;
}

/* set2 容器样式 */
.set2-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 10px 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 183, 197, 0.4) rgba(255, 255, 255, 0.05);
}

.set2-container::-webkit-scrollbar {
  width: 4px;
}

.set2-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin: 10px 0;
}

.set2-container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 183, 197, 0.4);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.set2-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 183, 197, 0.6);
}

.set2-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 15px;
  align-items: center;
  width: 97%;
  margin-left: 15px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  justify-content: center;
}

.set2-text {
  color: #e0e0e0;
  font-size: 1rem;
  line-height: 1.6;
  word-wrap: break-word;
  text-align: justify;
  padding-right: 10px;
}

.set2-button,
.set3-button,
.set4-button {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 183, 197, 0.7) 0%, rgba(255, 158, 181, 0.7) 100%);
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  flex-shrink: 0;
  padding: 0;
  margin: 0;
  position: relative;
  box-shadow: 0 2px 8px rgba(255, 183, 197, 0.2);
}

.set2-button::before,
.set3-button::before,
.set4-button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
  z-index: 0;
}

.set2-button:hover,
.set3-button:hover,
.set4-button:hover {
  background: linear-gradient(135deg, rgba(255, 183, 197, 0.95) 0%, rgba(255, 158, 181, 0.95) 100%);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 6px 20px rgba(255, 183, 197, 0.5), 0 0 15px rgba(255, 183, 197, 0.3);
}

.set2-button:hover::before,
.set3-button:hover::before,
.set4-button:hover::before {
  width: 100%;
  height: 100%;
}

/* set3 容器样式 (github项目列表) */
.set3-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 10px 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 183, 197, 0.4) rgba(255, 255, 255, 0.05);
}

.set3-container::-webkit-scrollbar {
  width: 4px;
}

.set3-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin: 10px 0;
}

.set3-container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 183, 197, 0.4);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.set3-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 183, 197, 0.6);
}

.set3-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 15px;
  align-items: center;
  width: 97%;
  margin-left: 15px;
}

.set3-text {
  color: #e0e0e0;
  font-size: 1rem;
  line-height: 1.6;
  word-wrap: break-word;
  text-align: justify;
  padding-right: 10px;
}


/* set4 容器样式 (producthunt项目列表) */
.set4-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 10px 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 183, 197, 0.4) rgba(255, 255, 255, 0.05);
}

.set4-container::-webkit-scrollbar {
  width: 4px;
}

.set4-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin: 10px 0;
}

.set4-container::-webkit-scrollbar-thumb {
  background-color: rgba(255, 183, 197, 0.4);
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.set4-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 183, 197, 0.6);
}

.set4-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 15px;
  align-items: center;
  width:  97%;
  margin-left: 15px;
}

.set4-text {
  color: #e0e0e0;
  font-size: 1rem;
  line-height: 1.6;
  word-wrap: break-word;
  text-align: justify;
  padding-right: 10px;
}

/* 特效按钮样式 */
.set2-effect-button,
.set3-effect-button,
.set4-effect-button {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 183, 197, 0.8) 0%, rgba(255, 158, 181, 0.8) 100%);
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  flex-shrink: 0;
  padding: 0;
  margin: 0;
  position: relative;
  box-shadow: 0 2px 8px rgba(255, 183, 197, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #500724;
  font-weight: bold;
}

.set2-effect-button::before,
.set3-effect-button::before,
.set4-effect-button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
  z-index: 0;
}

.set2-effect-button:hover,
.set3-effect-button:hover,
.set4-effect-button:hover {
  background: linear-gradient(135deg, rgba(255, 183, 197, 1) 0%, rgba(255, 158, 181, 1) 100%);
  border-color: rgba(255, 255, 255, 0.6);
  box-shadow: 0 6px 20px rgba(255, 183, 197, 0.6), 0 0 15px rgba(255, 183, 197, 0.4);
  transform: scale(1.1) rotate(10deg);
}

.set2-effect-button:hover::before,
.set3-effect-button:hover::before,
.set4-effect-button:hover::before {
  width: 100%;
  height: 100%;
}

/* 文本高亮标记特效 */
.set2-text.highlight-effect,
.set3-text.highlight-effect,
.set4-text.highlight-effect {
  position: relative;
  z-index: 10;
}

.set2-text.highlight-effect::before,
.set3-text.highlight-effect::before,
.set4-text.highlight-effect::before {
  content: "";
  position: absolute;
  top: -8px;
  left: -12px;
  right: -12px;
  bottom: -8px;
  background: linear-gradient(
    135deg,
    rgba(255, 183, 197, 0.10) 0%,
    rgba(255, 158, 181, 0.10) 50%,
    rgba(255, 183, 197, 0.10) 100%
  );
  background-size: 200% 100%;
  border-radius: 8px;
  box-shadow: 
    0 0 20px rgba(255, 183, 197, 0.3),
    0 0 40px rgba(255, 183, 197, 0.15),
    inset 0 0 15px rgba(255, 183, 197, 0.1);
  outline: 2px solid rgba(255, 183, 197, 0.5);
  outline-offset: -2px;
  z-index: -1;
  animation: highlightPulse 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  pointer-events: none;
}

@keyframes highlightPulse {
  0% {
    box-shadow: 
      0 0 0 rgba(255, 183, 197, 0),
      0 0 0 rgba(255, 183, 197, 0),
      inset 0 0 0 rgba(255, 183, 197, 0);
    outline-color: rgba(255, 183, 197, 0);
  }
  50% {
    box-shadow: 
      0 0 25px rgba(255, 183, 197, 0.4),
      0 0 50px rgba(255, 183, 197, 0.2),
      inset 0 0 20px rgba(255, 183, 197, 0.15);
    outline-color: rgba(255, 183, 197, 0.6);
  }
  100% {
    box-shadow: 
      0 0 20px rgba(255, 183, 197, 0.3),
      0 0 40px rgba(255, 183, 197, 0.15),
      inset 0 0 15px rgba(255, 183, 197, 0.1);
    outline-color: rgba(255, 183, 197, 0.5);
  }
}


@keyframes shimmer {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 200% 50%;
  }
}

.set2-text.highlight-effect::after,
.set3-text.highlight-effect::after,
.set4-text.highlight-effect::after {
  content: "✨";
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 14px;
  animation: sparkle 2s ease-in-out infinite;
  z-index: 11;
  opacity: 0.7;
}

@keyframes sparkle {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
  50% {
    transform: scale(1.3) rotate(180deg);
    opacity: 0.8;
  }
}

/* 写入文件按钮容器 */
.write-file-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  margin-bottom: 20px;
}

/* 写入文件按钮样式 */
.write-file-button {
  padding: 15px 40px;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff9eb5 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 8px 20px rgba(255, 183, 197, 0.4), 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.write-file-button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 0;
}

.write-file-button:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 15px 35px rgba(255, 183, 197, 0.6), 0 8px 15px rgba(0, 0, 0, 0.3);
}

.write-file-button:hover::before {
  width: 300px;
  height: 300px;
}

.write-file-button:active {
  transform: translateY(-1px) scale(1.02);
}

.write-file-button span {
  position: relative;
  z-index: 1;
}

/* set2写入文件按钮容器 */
.set2-write-file-container {
  display: flex;
  justify-content: center;
  padding: 15px 0;
  margin-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* set2写入文件按钮样式 */
.set2-write-file-button {
  padding: 10px 30px;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff9eb5 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 6px 15px rgba(255, 183, 197, 0.4), 0 3px 6px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.set2-write-file-button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 0;
}

.set2-write-file-button:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 10px 25px rgba(255, 183, 197, 0.6), 0 5px 10px rgba(0, 0, 0, 0.3);
}

.set2-write-file-button:hover::before {
  width: 200px;
  height: 200px;
}

.set2-write-file-button:active {
  transform: translateY(0) scale(1.02);
}

.set2-write-file-button span {
  position: relative;
  z-index: 1;
}

/* set3写入文件按钮容器 */
.set3-write-file-container {
  display: flex;
  justify-content: center;
  padding: 15px 0;
  margin-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* set3写入文件按钮样式 */
.set3-write-file-button {
  padding: 10px 30px;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff9eb5 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 6px 15px rgba(255, 183, 197, 0.4), 0 3px 6px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.set3-write-file-button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 0;
}

.set3-write-file-button:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 10px 25px rgba(255, 183, 197, 0.6), 0 5px 10px rgba(0, 0, 0, 0.3);
}

.set3-write-file-button:hover::before {
  width: 200px;
  height: 200px;
}

.set3-write-file-button:active {
  transform: translateY(0) scale(1.02);
}

.set3-write-file-button span {
  position: relative;
  z-index: 1;
}

/* set4写入文件按钮容器 */
.set4-write-file-container {
  display: flex;
  justify-content: center;
  padding: 15px 0;
  margin-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* set4写入文件按钮样式 */
.set4-write-file-button {
  padding: 10px 30px;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff9eb5 100%);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 6px 15px rgba(255, 183, 197, 0.4), 0 3px 6px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.set4-write-file-button::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
  z-index: 0;
}

.set4-write-file-button:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 10px 25px rgba(255, 183, 197, 0.6), 0 5px 10px rgba(0, 0, 0, 0.3);
}

.set4-write-file-button:hover::before {
  width: 200px;
  height: 200px;
}

.set4-write-file-button:active {
  transform: translateY(0) scale(1.02);
}

.set4-write-file-button span {
  position: relative;
  z-index: 1;
}


</style>

