document.addEventListener('DOMContentLoaded', () => {
    const openModalButton = document.getElementById('open-note-modal');
    const modal = document.getElementById('note-modal');
    const closeModalButton = document.querySelector('#note-modal .close-button');
    const noteForm = document.getElementById('note-form');
    const alertBox = document.createElement('div'); // Create a div for alert messages

    //Open Modal
    openModalButton.addEventListener('click', () => {
        modal.classList.remove('hidden');
        if (modal.querySelector('.modal-content').scrollHeight > modal.querySelector('.modal-content').clientHeight) {
        modal.querySelector('.modal-content').classList.add('scrollable');
    }
    });

    //Close Modal
    closeModalButton.addEventListener('click', () => {
        modal.classList.add('hidden');
        alertBox.remove(); // Remove alert messages when closing the modal
    });

    //Close Modal if click outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
            alertBox.remove(); // Remove alert messages when closing the modal
        }
    })

    //Handle form submission (using fetch)
    noteForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(noteForm);
        // const alertBox = document.createElement('div');
        try {
            const response = await fetch(noteCreateUrl, {
                method: 'POST',
                body: formData,
        });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Success:', data);
            alertBox.className = 'alert alert-success';
            alertBox.textContent = data.message;
            modal.appendChild(alertBox); // Append to modal
            setTimeout(() => {
                alertBox.remove();
                modal.classList.add('hidden');
            }, 2000);
        } catch (error) {
            console.error('Error:', error);
            //More robust error handling:
            let errorMessage = '시음 노트 저장에 실패했습니다.';
            if(error.message.startsWith('HTTP error!')){
                errorMessage = `HTTP 에러: ${error.message.split(':')[1].trim()}`;
            } else if (error instanceof SyntaxError){
                errorMessage = '잘못된 서버 응답: JSON 데이터가 아닙니다.';
            }

            alertBox.className = 'alert alert-danger';
            alertBox.textContent = errorMessage;
            modal.appendChild(alertBox); // Append to modal
        }
    });
});