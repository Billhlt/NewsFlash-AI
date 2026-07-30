const SPRINGAI_URL = 'http://localhost:8081'
const PYTHON_URL = 'http://localhost:8000'

/**
 * 聊天相关的API接口定义模块
 * 该模块导出了一个包含聊天相关API方法的对象
 * export是js文件的特例，python文件中不加也可以导到其他模块，js则必须加才能到vue文件中
 */
export const chatAPI = {
  // 发送聊天消息
  // 异步发送消息
  async sendMessage(data, chatId) {
    try {
      // 创建URL对象
      const url = new URL(`${SPRINGAI_URL}/ai/chat`)
      // 如果有chatId，则添加到URL参数中
      if (chatId) {
        url.searchParams.append('chatId', chatId)
      }
      
      // 发送POST请求
      const response = await fetch(url, {
        method: 'POST',
        body: data instanceof FormData ? data : 
          new URLSearchParams({ prompt: data })
      })

      // 如果响应状态码不是200，则抛出错误
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // 返回响应体读取器
      return response.body.getReader()
    } catch (error) {
      // 打印错误信息
      console.error('API Error:', error)
      // 抛出错误
      throw error
    }
  },

  // 获取聊天历史列表
  async getChatHistory(type = 'chat') {  // 添加类型参数
    try {
      const response = await fetch(`${SPRINGAI_URL}/ai/history/${type}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const chatIds = await response.json()
      // 转换为前端需要的格式
      return chatIds.map(id => ({
        id,
        title: type === 'pdf' ? `PDF对话 ${id.slice(-6)}` : 
               type === 'service' ? `咨询 ${id.slice(-6)}` :
               `对话 ${id.slice(-6)}`
      }))
    } catch (error) {
      console.error('API Error:', error)
      return []
    }
  },

  // 获取特定对话的消息历史
  async getChatMessages(chatId, type = 'chat') {  // 添加类型参数
    try {
      const response = await fetch(`${SPRINGAI_URL}/ai/history/${type}/${chatId}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const messages = await response.json()
      // 添加时间戳
      return messages.map(msg => ({
        ...msg,
        timestamp: new Date() // 由于后端没有提供时间戳，这里临时使用当前时间
      }))
    } catch (error) {
      console.error('API Error:', error)
      return []
    }
  },

} 


import axios from 'axios';


// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000', // 你的FastAPI服务器地址
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 函数名后面有01代表重点公众号文章的接口，02代表非重点公众号文章的接口
// 获取总结内容01
export const getSummary01 = () => {
  return api.get('/api/summary01');
};

// 获取词语位置01
export const getWordPosition01 = () => {
  return api.get('/api/wordposition01');
};

// 获取url01
export const getUrl01 = () => {
  return api.get('/api/url01');
};

// 获取url02
export const getUrl02 = () => {
  return api.get('/api/url02');
};

// 获取总结内容02
export const getSummary02 = () => {
  return api.get('/api/summary02');
};

// // 获取词语位置02
// export const getWordPosition02 = () => {
//   return api.get('/api/wordposition02');
// };

// 获取producthunt热榜
export const getProducthunt = () => {
  return api.get('/api/producthunt');
};

// 获取producthunt链接
export const getProducthuntUrls = () => {
  return api.get('/api/producthunt_urls');
};

// 获取github热榜
export const getGithub = () => {
  return api.get('/api/github');
};

// 获取github名称
export const getGithubName = () => {
  return api.get('/api/github_name');
};

// 写入文本到文件
export const writeTextsToFile = (texts) => {
  return api.post('/api/write_texts_to_file', { texts });
};

// 写入文本到github项目整理文件
export const writeTextsToGithubFile = (texts) => {
  return api.post('/api/write_texts_to_github_file', { texts });
};

// 写入文本到producthunt产品整理文件
export const writeTextsToProducthuntFile = (texts) => {
  return api.post('/api/write_texts_to_producthunt_file', { texts });
};



