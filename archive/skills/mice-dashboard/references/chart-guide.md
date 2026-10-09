# 차트 유형 선택 가이드

## Chart.js 차트 유형별 활용 가이드

### 1. 바 차트 (Bar Chart)
**적합한 데이터**: 카테고리별 수치 비교
**사용 시점**: 항목 간 크기를 직관적으로 비교할 때
**설정 팁**:
```javascript
{
  type: 'bar',
  options: {
    indexAxis: 'x',  // 'y'로 변경하면 수평 바
    plugins: {
      tooltip: {
        callbacks: {
          label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y.toLocaleString('ko-KR')}명`
        }
      }
    },
    scales: {
      y: { beginAtZero: true, ticks: { callback: v => v.toLocaleString('ko-KR') } }
    }
  }
}
```
**바 5개 이하**: 수직 바 / **바 6개 이상 또는 레이블 긴 경우**: 수평 바

### 2. 라인 차트 (Line Chart)
**적합한 데이터**: 시계열, 추세, 변화량
**사용 시점**: 시간 흐름에 따른 변화를 보여줄 때
**설정 팁**:
```javascript
{
  type: 'line',
  options: {
    tension: 0.3,       // 부드러운 곡선
    fill: true,          // 영역 채우기
    pointRadius: 4,
    pointHoverRadius: 6
  }
}
```
**라인 3개 이하** 권장. 초과 시 가독성 저하.

### 3. 도넛 차트 (Doughnut Chart)
**적합한 데이터**: 구성 비율, 점유율
**사용 시점**: 전체 대비 각 항목의 비중을 보여줄 때
**설정 팁**:
```javascript
{
  type: 'doughnut',
  options: {
    cutout: '60%',
    plugins: {
      tooltip: {
        callbacks: {
          label: (ctx) => {
            const pct = ((ctx.parsed / ctx.dataset.data.reduce((a,b)=>a+b,0)) * 100).toFixed(1);
            return `${ctx.label}: ${pct}%`;
          }
        }
      }
    }
  }
}
```
**항목 6개 이하** 권장. 초과 시 '기타'로 묶기.

### 4. 레이더 차트 (Radar Chart)
**적합한 데이터**: 다차원 평가, 역량 비교
**사용 시점**: 여러 평가 항목을 한눈에 비교할 때 (만족도 항목별 점수 등)
**설정 팁**:
```javascript
{
  type: 'radar',
  options: {
    scales: {
      r: {
        min: 0,
        max: 5,  // 또는 100 (데이터 범위에 맞춤)
        ticks: { stepSize: 1 }
      }
    }
  }
}
```
**축 4~8개** 권장.

### 5. 스택드 바 차트 (Stacked Bar)
**적합한 데이터**: 구성 요소별 누적 비교
**사용 시점**: 비용 항목별 구성을 비교할 때
**설정 팁**:
```javascript
{
  type: 'bar',
  options: {
    scales: {
      x: { stacked: true },
      y: { stacked: true }
    }
  }
}
```

### 6. 혼합 차트 (Mixed Chart)
**적합한 데이터**: 서로 다른 단위의 데이터를 한 차트에
**사용 시점**: 매출(바) + 성장률(라인) 같은 이중 축이 필요할 때
**설정 팁**:
```javascript
{
  type: 'bar',
  data: {
    datasets: [
      { type: 'bar', label: '매출', yAxisID: 'y' },
      { type: 'line', label: '성장률', yAxisID: 'y1' }
    ]
  },
  options: {
    scales: {
      y: { position: 'left', title: { display: true, text: '매출 (억원)' } },
      y1: { position: 'right', title: { display: true, text: '성장률 (%)' }, grid: { drawOnChartArea: false } }
    }
  }
}
```

## 컬러 팔레트

### 다크 모드 (프리미엄)
```javascript
const DARK_COLORS = {
  bg: '#0A2540',
  card: '#1A1D24',
  cardBorder: '#5A6270',
  text: '#F1F3F7',
  textSecondary: '#A0A6B0',
  accent: '#2962FF',
  positive: '#00E676',
  negative: '#D32F2F',
  chart: ['#2962FF', '#E91E63', '#2962FF', '#FFA000', '#E91E63', '#00C853']
};
```

### 라이트 모드 (비즈니스)
```javascript
const LIGHT_COLORS = {
  bg: '#F8F9FB',
  card: '#ffffff',
  cardBorder: '#E5E8ED',
  text: '#1A1D24',
  textSecondary: '#5A6270',
  accent: '#2962FF',
  positive: '#00C853',
  negative: '#D32F2F',
  chart: ['#2962FF', '#E91E63', '#1E4DCC', '#FF5722', '#E91E63', '#00C853']
};
```

### 컬러풀 모드 (이벤트/마케팅)
```javascript
const EVENT_COLORS = {
  bg: '#F8F9FB',
  card: '#ffffff',
  cardBorder: '#E5E8ED',
  text: '#0A2540',
  textSecondary: '#5A6270',
  accent: '#E91E63',
  positive: '#00C853',
  negative: '#D32F2F',
  chart: ['#E91E63', '#FFA000', '#E91E63', '#00E676', '#FF5722', '#E91E63']
};
```

## 디자인 톤 자동 결정 로직

```
IF 데이터에 '보고', '결과', '실적', 'report' 키워드가 포함됨
  → 다크 모드 (프리미엄, 공식 보고 느낌)
ELSE IF 데이터에 '매출', '비용', '예산', '수익', 'revenue', 'cost' 키워드 위주
  → 라이트 모드 (비즈니스, 깔끔하고 신뢰감)
ELSE IF 데이터에 '이벤트', '페스티벌', '캠페인', '마케팅' 키워드 포함
  → 컬러풀 모드 (에너지, 역동적)
ELSE
  → 라이트 모드 (기본값, 가장 범용적)
```

## 숫자 포맷 유틸리티

대시보드에서 사용할 한국어 숫자 포맷 함수:

```javascript
function formatKR(value, type) {
  if (value === null || value === undefined) return '-';
  switch(type) {
    case 'number':
      return value.toLocaleString('ko-KR');
    case 'currency':
      if (value >= 100000000) return `${(value/100000000).toFixed(1)}억원`;
      if (value >= 10000) return `${(value/10000).toFixed(0)}만원`;
      return `${value.toLocaleString('ko-KR')}원`;
    case 'percent':
      return `${value.toFixed(1)}%`;
    case 'people':
      if (value >= 10000) return `${(value/10000).toFixed(1)}만명`;
      return `${value.toLocaleString('ko-KR')}명`;
    default:
      return value.toLocaleString('ko-KR');
  }
}
```

## 차트 공통 설정

모든 차트에 적용할 Chart.js 글로벌 설정:

```javascript
Chart.defaults.font.family = "'Pretendard', -apple-system, sans-serif";
Chart.defaults.font.size = 13;
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.animation.duration = 800;
Chart.defaults.animation.easing = 'easeOutQuart';
```
