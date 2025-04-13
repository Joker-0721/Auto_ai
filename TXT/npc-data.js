const NPC_TEMPLATES = {
  names: ['林阿寶', '陳春花', '黃大牛', '王明月', '張鐵柱', '李金鳳', '吳天賜', '周美玉', '徐志強', '鄭秀蘭'],
  surnames: ['林', '陳', '黃', '王', '張', '李', '吳', '周', '徐', '鄭'], // 新增姓氏庫
  occupations: ['茶農', '藥師', '鐵匠', '書生', '漁夫', '織女', '獵戶', '廚娘', '算命師', '木匠'],
  dialogs: {
    morning: ['今天天氣真適合採茶！', '要來杯剛泡好的烏龍嗎？', '山上的竹子長得可好了'],
    afternoon: ['午後最適合編竹簍了', '這把新打的柴刀特別鋒利', '聽過後山的傳說嗎？'],
    evening: ['星星出來前得收完草藥', '今晚村口有說書人來', '早點休息明天還要磨豆子']
  },
  skills: {
    types: ['農業', '手工藝', '學識', '戰鬥', '醫術'],
    baseValues: {
      // 补充完整职业基础数值
      '茶農': { '農業': 70, '手工藝': 40 },
      '藥師': { '醫術': 85, '學識': 60 },
      '鐵匠': { '手工藝': 80, '戰鬥': 30 },
      '書生': { '學識': 90, '農業': 20 },
      '漁夫': { '戰鬥': 50, '農業': 30 },
      '織女': { '手工藝': 85, '學識': 40 },
      '獵戶': { '戰鬥': 75, '醫術': 35 },
      '廚娘': { '手工藝': 70, '農業': 45 },
      '算命師': { '學識': 80, '醫術': 50 },
      '木匠': { '手工藝': 85, '農業': 30 }
    }
  },
  inventoryItems: [
    // 补充更多职业相关物品
    { name: '漁網', type: '工具', value: 45 },
    { name: '醫書', type: '書籍', value: 80 },
    { name: '鐵礦石', type: '材料', value: 30 },
    { name: '文房四寶', type: '工具', value: 120 },
    { name: '絲綢', type: '材料', value: 65 }
  ],
  dailyActivities: {
    morning: ['採茶', '鍛造', '讀書', '捕魚'],
    afternoon: ['市集交易', '授課', '練武', '採藥'],
    evening: ['酒館社交', '家庭聚餐', '個人修煉', '夜間巡邏']
  }
};

const generateNPCs = () => {
  const npcs = [];
  const usedNames = new Set();
  
  for(let i = 0; i < 50; i++) {
    const getUniqueName = () => {
      let name = NPC_TEMPLATES.names[Math.floor(Math.random() * NPC_TEMPLATES.names.length)];
      while(usedNames.has(name)) {
        name += String.fromCharCode(0x3041 + Math.random() * 96);
      }
      usedNames.add(name);
      return name;
    };
    
    npcs.push({
      id: `npc_${i + 1}`,
      name: getUniqueName(),
      age: Math.floor(16 + Math.random() * 60), // 新增年齡屬性
      gender: Math.random() > 0.5 ? 'male' : 'female', // 新增性別屬性
      occupation: (() => {
        const occupation = NPC_TEMPLATES.occupations[Math.floor(Math.random() * NPC_TEMPLATES.occupations.length)];
        return occupation;
      })(),
      skills: generateSkills((() => {
        const occupation = NPC_TEMPLATES.occupations[Math.floor(Math.random() * NPC_TEMPLATES.occupations.length)];
        return occupation;
      })()),
      avatar: `https://picsum.photos/200/300?${gender === 'male' ? 'men' : 'women'}=${i}`, // 根據性別優化頭像
      dialogs: {
        morning: NPC_TEMPLATES.dialogs.morning[Math.floor(Math.random() * NPC_TEMPLATES.dialogs.morning.length)],
        afternoon: NPC_TEMPLATES.dialogs.afternoon[Math.floor(Math.random() * NPC_TEMPLATES.dialogs.afternoon.length)],
        evening: NPC_TEMPLATES.dialogs.evening[Math.floor(Math.random() * NPC_TEMPLATES.dialogs.evening.length)]
      },
      traits: { // 改為分層特徵系統
        personality: ['好奇', '幽默', '嚴肅', '熱心', '沉默'],
        background: ['世家子弟', '戰爭孤兒', '江湖遊俠', '歸隱高人', '書香傳家']
      }, // 補上逗號
      skills: generateSkills(occupation),  // 新增技能系統
      // 移除多餘的 getter/setter 定義
      inventory: generateInventory(occupation),  
      schedule: generateDailySchedule(occupation),  // 新增行為模式
      economy: {
        money: Math.floor(Math.random() * 1000) + 500,  // 初始資金
        debt: 0
      },
      dialogs: generateTraitBasedDialogs(traits)  // 強化對話系統
    });
  }
  return npcs;
};

// 新增輔助函式
const pickRandom = (arr, count) => {
  return [...arr].sort(() => 0.5 - Math.random()).slice(0, count);
};

const generateRelationships = (existingNPCs) => {
  return existingNPCs.slice(0, Math.floor(Math.random() * 3)).map(npc => ({
    id: npc.id,
    type: ['family', 'friend', 'rival'][Math.floor(Math.random() * 3)]
  }));
};

const VILLAGE_NPCS = [
  {
    name: '艾莉絲',
    occupation: '鐵匠',
    avatar: 'blacksmith.png',
    traits: '勤勞|固執',
    schedule: {
      7: {state: '工作', location: '鐵匠舖'},
      12: {state: '休息', location: '市集'},
      18: {state: '回家', location: '住宅區'}
    },
    waypoints: ['鐵匠舖', '市集', '中央廣場', '住宅區']
  },

// 新增技能生成函式
const generateSkills = function(occupation) {
  const base = NPC_TEMPLATES.skills.baseValues[occupation] || {};
  return NPC_TEMPLATES.skills.types.map(skill => ({
    name: skill,
    level: (base[skill] || 20) + Math.floor(Math.random() * 20)
  }));
};

// 新增特徵對話生成函式
const generateTraitBasedDialogs = (traits) => {
  const personalityDialogs = {
    '幽默': ['你知道為什麼雞過馬路嗎？', '生活就像茶葉，總要浮沉幾次'],
    '嚴肅': ['萬事皆須謹慎', '言行當思後果']
  };
  
  return {
    morning: selectDialogBasedOnTraits(NPC_TEMPLATES.dialogs.morning, traits),
    // 其他時段對話生成...
  };
};

// 新增物品生成函式
const generateInventory = (occupation) => {
  return [...NPC_TEMPLATES.inventoryItems]
    .filter(item => item.type === '工具')
    .slice(0, 2)
    .concat({
      name: `${occupation}工作證`,
      type: '身份證明',
      value: 100
    });
};

// 新增行為模式生成函式
const generateDailySchedule = (occupation) => {
  const getActivity = (time) => {
    const activities = NPC_TEMPLATES.dailyActivities[time];
    return activities.find(a => a.includes(occupation[0])) || 
           activities[Math.floor(Math.random() * activities.length)];
  };

  return {
    morning: getActivity('morning'),
    afternoon: getActivity('afternoon'),
    evening: getActivity('evening')
  };
};

// 在 generateTraitBasedDialogs 补充完整
function generateTraitBasedDialogs(traits) {
  const backgroundDialogs = {
    '世家子弟': { afternoon: ['家父常說經商之道在於誠信', '這玉佩是家傳之寶'] },
    '戰爭孤兒': { evening: ['小時候常躲在穀倉過夜', '能活著就是福氣'] }
  };

  return {
    morning: selectDialogBasedOnTraits(NPC_TEMPLATES.dialogs.morning, traits),
    afternoon: selectDialogBasedOnTraits(NPC_TEMPLATES.dialogs.afternoon, traits),
    evening: selectDialogBasedOnTraits(NPC_TEMPLATES.dialogs.evening, traits),
    ...(backgroundDialogs[traits.background[0]] || {})
  };
};

// 新增對話選擇函式 (需添加在文件頂部)
const selectDialogBasedOnTraits = (dialogs, traits) => {
  const traitDialogs = dialogs.filter(d => 
    traits.personality.some(p => d.includes(p)) ||
    traits.background.some(b => d.includes(b))
  );
  return traitDialogs.length > 0 
    ? traitDialogs[Math.floor(Math.random() * traitDialogs.length)]
    : dialogs[Math.floor(Math.random() * dialogs.length)];
};