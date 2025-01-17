document.addEventListener("DOMContentLoaded", function () {

    const noteForm = document.getElementById('note-form');
    const prevBtn = document.querySelector('.btn-prev');
    const nextBtn = document.querySelector('.btn-next');
    const steps = document.querySelectorAll('.step');
    const stepContents = document.querySelectorAll('.step-content');
    const btnPrev = document.querySelector('.btn-prev');
    const btnNext = document.querySelector('.btn-next');
    const btnSave = document.querySelector('.btn-save');
    let currentStep = 1;

    // 스텝 네비게이션 함수
    function updateNavigation() {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index + 1 <= currentStep);
        });
        prevBtn.style.display = currentStep === 1 ? 'none' : 'inline-flex';
        
        if (currentStep === steps.length) {
            nextBtn.innerHTML = '<i class="fas fa-check"></i> 완료';
        } else {
            nextBtn.innerHTML = '다음 <i class="fas fa-arrow-right"></i>';
        }
        stepContents.forEach((content, index) => {
            content.style.display = index + 1 === currentStep ? 'block' : 'none';
        });
    }

    // Step 업데이트 함수
    function updateSteps() {
        steps.forEach((step, index) => {
            step.classList.toggle('active', index === currentStep);
        });
        stepContents.forEach((content, index) => {
            content.style.display = index === currentStep ? 'block' : 'none';
        });
        btnPrev.style.display = currentStep === 0 ? 'none' : 'inline-block';
        btnNext.style.display = currentStep === steps.length - 1 ? 'none' : 'inline-block';
    }

    // 이벤트 리스너 설정
    steps.forEach(step => {
        step.addEventListener('click', function() {
            const stepNum = parseInt(this.dataset.step);
            if (stepNum) {
                currentStep = stepNum;
                updateNavigation();
            }
        });
    });
    prevBtn?.addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            updateNavigation();
        }
    });
    nextBtn?.addEventListener('click', () => {
        if (currentStep < steps.length) {
            currentStep++;
            updateNavigation();
        }
    });

    // Step 번호 클릭 이벤트
    steps.forEach((step, index) => {
        step.addEventListener('click', () => {
            currentStep = index;
            updateSteps(currentStep);
        });
    });

    btnNext.addEventListener('click', () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateSteps(currentStep);
        }
    });
    // 초기 네비게이션 상태 설정
    updateNavigation();

    // 초기 Step 설정
    updateSteps();

    // 저장 버튼 클릭 이벤트
    btnSave.addEventListener('click', () => {
        form.submit();
    });

    if (btnPrev) {
        btnPrev.addEventListener('click', () => {
            console.log('이전 버튼 클릭');
        });
    } else {
        console.warn('이전 버튼이 존재하지 않습니다.');
    }

    if (btnNext) {
        btnNext.addEventListener('click', () => {
            console.log('다음 버튼 클릭');
        });
    } else {
        console.warn('다음 버튼이 존재하지 않습니다.');
    }

    // ** 슬라이더 초기화 함수 **
    const sliderConfigs = {
        appearance_intensity: ['매우 연함', '연함', '보통', '진함', '매우 진함'],
        appearance_clarity: ['탁함', '약간 탁함', '맑음', '매우 맑음', '투명함'],
        aroma_intensity: ['매우 약함', '약함', '보통', '강함', '매우 강함'],
        sweetness: ['드라이', '약간 드라이', '중간', '약간 달콤', '달콤'],
        acidity: ['매우 낮음', '낮음', '중간', '높음', '매우 높음'],
        tannin: ['매우 부드러움', '부드러움', '중간', '강함', '매우 강함'],
        body: ['매우 가벼움', '가벼움', '중간', '무거움', '매우 무거움'],
    };

    // 슬라이더 초기화 함수
    function initSliders() {
        const sliderConfigs = {
            appearance_intensity: 'appearance_intensity',
            appearance_clarity: 'appearance_clarity',
            aroma_intensity: 'aroma_intensity',
            sweetness: 'sweetness',
            acidity: 'acidity',
            tannin: 'tannin',
            body: 'body',
        };

        Object.entries(sliderConfigs).forEach(([sliderId, hiddenInputId]) => {
        const sliderElement = document.getElementById(`${sliderId}-slider`);
        const hiddenInput = document.getElementById(hiddenInputId);

        if (!sliderElement || !hiddenInput) {
            console.warn(`슬라이더 또는 hidden input이 존재하지 않습니다: ${sliderId}`);
            return; // 해당 슬라이더 초기화를 건너뜀
        }

        noUiSlider.create(sliderElement, {
            start: 3,
            connect: 'lower',
            step: 1,
            range: {
                min: 1,
                max: 5,
            },
        });

        sliderElement.noUiSlider.on('update', (values) => {
            const value = Math.round(values[0]);
            hiddenInput.value = value; // hidden input 값 업데이트
        });
    });
}


// 디버깅용 로그 추가
console.log('슬라이더 초기화 시작');
Object.entries(sliderConfigs).forEach(([sliderId, hiddenInputId]) => {
    const sliderElement = document.getElementById(`${sliderId}-slider`);
    const hiddenInput = document.getElementById(hiddenInputId);
    if (!sliderElement) console.warn(`슬라이더가 없습니다: ${sliderId}-slider`);
    if (!hiddenInput) console.warn(`hidden input이 없습니다: ${hiddenInputId}`);
});

    // DOMContentLoaded 이벤트에서 슬라이더 초기화 호출
    document.addEventListener('DOMContentLoaded', initSliders);

    // ** 품종 관리 초기화 **
    function initGrapeVarietyManagement() {
        const grapeTags = document.getElementById("grape_tags");
        const grapeInput = document.getElementById("grape_variety_input");
        const addGrapeBtn = document.getElementById("add_grape_btn");
        const grapeVarietiesInput = document.getElementById("grape_varieties");

        function updateGrapeTags() {
            const tags = Array.from(grapeTags.querySelectorAll(".grape-tag")).map(
                (tag) => tag.textContent.trim()
            );
            grapeVarietiesInput.value = JSON.stringify(tags);
        }

        addGrapeBtn.addEventListener("click", function () {
            const value = grapeInput.value.trim();
            if (value) {
                const tag = document.createElement("span");
                tag.className = "grape-tag";
                tag.textContent = value;
                const removeBtn = document.createElement("button");
                removeBtn.textContent = "×";
                removeBtn.addEventListener("click", function () {
                    tag.remove();
                    updateGrapeTags();
                });
                tag.appendChild(removeBtn);
                grapeTags.appendChild(tag);
                grapeInput.value = "";
                updateGrapeTags();
            }
        });
    }

    initGrapeVarietyManagement(); // 품종 관리 초기화 실행


    // ** 음식 페어링 스크립트 **
    const foodInput = document.getElementById('food_pairing_input');
    const selectedFoodTags = document.getElementById('selected-food-tags');
    const foodPairingsHidden = document.getElementById('food_pairings_hidden');
    const presetTags = document.querySelectorAll('.food-tag');
    let selectedFoods = new Set();

    function updateFoodTags() {
        selectedFoodTags.innerHTML = Array.from(selectedFoods)
            .map(
                (food) =>
                    `<span class="selected-tag">
                        ${food}
                        <button type="button" onclick="removeFood('${food}')">&times;</button>
                    </span>`
            )
            .join('');
        foodPairingsHidden.value = JSON.stringify(Array.from(selectedFoods));
    }

    presetTags.forEach((tag) => {
        tag.addEventListener('click', function () {
            const value = this.dataset.value;
            if (this.classList.toggle('selected')) {
                selectedFoods.add(value);
            } else {
                selectedFoods.delete(value);
            }
            updateFoodTags();
        });
    });

    foodInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const value = foodInput.value.trim();
            if (value && !selectedFoods.has(value)) {
                selectedFoods.add(value);
                updateFoodTags();
                foodInput.value = '';
            }
        }
    });

    window.removeFood = function (food) {
        selectedFoods.delete(food);
        updateFoodTags();
    };


    const tasteNotesInput = document.getElementById("taste_notes_hidden");
    const tasteNoteTags = document.getElementById("taste-note-tags");
    const tasteInput = document.getElementById("taste_note_input");

    function updateTasteNotes() {
        const tags = Array.from(tasteNoteTags.querySelectorAll(".taste-tag")).map(
            (tag) => tag.textContent
        );
        if (tasteNotesInput) {
            tasteNotesInput.value = JSON.stringify(tags);
        } else {
            console.error("hidden input (taste_notes_hidden)이 존재하지 않습니다.");
        }
    }

    if (tasteInput) {
        tasteInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                const value = tasteInput.value.trim();
                if (value) {
                    const tag = document.createElement("span");
                    tag.textContent = value;
                    tag.className = "taste-tag";
                    tasteNoteTags.appendChild(tag);
                    updateTasteNotes();
                    tasteInput.value = "";
                }
            }
        });
    } else {
        console.error("taste_note_input 요소를 찾을 수 없습니다.");
    }

    // 초기 업데이트
    updateTasteNotes();


    // 폼 제출 시 데이터 확인
    const form = document.getElementById('tastingNoteForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        console.log('폼 데이터:', Object.fromEntries(formData));
        alert('폼이 제출되었습니다!');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('tastingNoteForm');

    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(form);
            // 슬라이더 값이 폼 데이터에 추가되었는지 확인
            const sliderFields = ['appearance_intensity', 'appearance_clarity', 'aroma_intensity', 'sweetness', 'acidity', 'tannin', 'body'];
            sliderFields.forEach((field) => {
                if (!formData.has(field)) {
                    console.warn(`슬라이더 값이 폼 데이터에 없습니다: ${field}`);
                }
            });

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    alert('시음 노트가 성공적으로 저장되었습니다.');

                    // 최초 작성일 확인
                    if (data.hide_example_section) {
                        // 예시 섹션 숨기기
                        const exampleSection = document.querySelector('.recent-notes');
                        if (exampleSection) {
                            exampleSection.style.display = 'none';
                        }
                    }

                    // 노트 상세 페이지로 리다이렉트
                    window.location.href = data.redirect_url || '/notes/';
                } else {
                    const errorData = await response.json();
                    console.error('폼 제출 오류:', errorData);
                    alert('노트 저장에 실패했습니다. 오류 내용을 확인하세요.');
                }
            } catch (error) {
                console.error('서버 요청 중 오류:', error);
                alert('서버 요청 중 오류가 발생했습니다.');
            }
        });
    } else {
        console.warn('폼 요소를 찾을 수 없습니다.');
    }
});
