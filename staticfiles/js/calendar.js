document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    const calendarEvents = JSON.parse(calendarEl.dataset.events);
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ko',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth'
        },
        events: function(info, successCallback, failureCallback) {
            const noteCounts = JSON.parse(document.getElementById('note-counts-data').textContent);
            const events = [];
            
            for (let date in noteCounts) {
                events.push({
                    title: `${noteCounts[date]}개`,
                    start: date,
                    display: 'background',
                    backgroundColor: '#6c5ce7'
                });
            }
            
            successCallback(events);
        },
        dateClick: function(info) {
            const dateStr = info.dateStr;
            const count = noteCounts[dateStr] || 0;

            if (count > 0) {
                showSelectedDateNotes(dateStr);
            } else {
                showNoteModal(dateStr);
            }
        }
    });
    
    calendar.render();

    // 작성 모달 표시
    const addNoteBtn = document.getElementById('add-note-btn');
    const createModal = document.getElementById('note-modal');
    
    addNoteBtn.onclick = function() {
        const today = new Date().toISOString().split('T')[0];
        showNoteModal(today);
    }

    // 모달 닫기 버튼들
    document.querySelectorAll('.close-button').forEach(button => {
        button.onclick = function() {
            this.closest('.modal').style.display = 'none';
        }
    });

    // 모달 외부 클릭시 닫기
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    }
});

// 노트 작성 모달 표시
function showNoteModal(date) {
    const modal = document.getElementById('note-modal');
    const dateInput = modal.querySelector('input[name="tasting_date"]');
    if (dateInput) {
        dateInput.value = date;
    }
    modal.style.display = 'block';
}

// 선택한 날짜의 노트 표시
function showSelectedDateNotes(dateStr, containerId = 'selected-date-notes') {
    fetch(`/notes/api/notes/${dateStr}/`)
        .then(response => response.json())
        .then(notes => {
            const container = document.querySelector(`#${containerId} .notes-cards-container`);
            const dateTitle = document.querySelector(`#${containerId} .date-title`);
            
            dateTitle.textContent = `${dateStr} 시음노트`;
            
            const notesHtml = notes.map(note => `
                <div class="note-card">
                    <div class="note-card-header">
                        <h4>${note.wine_name}</h4>
                        <span class="wine-badge ${note.wine_type.toLowerCase()}">${note.wine_type_display}</span>
                    </div>
                    <div class="rating-stars">
                        ${'★'.repeat(note.rating)}${'☆'.repeat(5-note.rating)}
                    </div>
                    <div class="taste-metrics">
                        <div class="metric">
                            <span>당도</span>
                            <div class="progress-bar">
                                <div class="progress" style="width: ${note.sweetness * 20}%"></div>
                            </div>
                        </div>
                        <div class="metric">
                            <span>산도</span>
                            <div class="progress-bar">
                                <div class="progress" style="width: ${note.acidity * 20}%"></div>
                            </div>
                        </div>
                        <div class="metric">
                            <span>탄닌</span>
                            <div class="progress-bar">
                                <div class="progress" style="width: ${note.tannin * 20}%"></div>
                            </div>
                        </div>
                        <div class="metric">
                            <span>바디</span>
                            <div class="progress-bar">
                                <div class="progress" style="width: ${note.body * 20}%"></div>
                            </div>
                        </div>
                    </div>
                    <button class="detail-btn" onclick="showNoteDetail(${note.id})">상세보기</button>
                </div>
            `).join('');
            
            container.innerHTML = notesHtml;
            document.getElementById(containerId).style.display = 'block';
        });
}



// 모달 닫기 이벤트
document.querySelectorAll('.close-button').forEach(button => {
    button.onclick = function() {
        this.closest('.modal').style.display = 'none';
    }
});

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
} 