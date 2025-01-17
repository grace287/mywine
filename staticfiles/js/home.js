document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const modal = document.getElementById('note-modal');
    const closeBtn = document.querySelector('.close-button');
    
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ko',
        selectable: true,
        dateClick: function(info) {
            // 선택된 날짜를 폼의 날짜 필드에 설정
            const dateInput = document.querySelector('input[name="tasting_date"]');
            if (dateInput) {
                dateInput.value = info.dateStr;
            }
            
            // 모달 열기
            modal.classList.remove('hidden');
            
            // 폼 action URL에 선택된 날짜 추가
            const form = document.getElementById('note-form');
            form.action = `/notes/create/?date=${info.dateStr}`;
        }
    });
    
    calendar.render();
    
    // 모달 닫기 버튼
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.classList.add('hidden');
        });
    }
    
    // 모달 외부 클릭 시 닫기
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.add('hidden');
        }
    });
});