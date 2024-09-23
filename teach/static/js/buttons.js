window.onload = function() {
    const hash = window.location.hash;
    if (hash) {
        const exerciseCard = document.querySelector(hash);
        if (exerciseCard) {
            // Scroll to the element smoothly
            exerciseCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

            // Calculate offset to center the element in the viewport
            const offset = (window.innerHeight - exerciseCard.getBoundingClientRect().height) / 2;
            window.scrollBy(0, -offset); // Adjust the scroll position
        }
    }
};

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function scrollToTop(){
    window.scrollTo(0, 0);
}

function deleteFromHard(exerciseId) {
    $.ajax({
        url: `/hard/${exerciseId}`,
        type: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function(response) {
            if (response.status === 'deleted') {
                console.log('Exercise deleted from pinned successfully:', exerciseId);

                // remove exercise from list of hard exercises
                $('#hard-exercise-' + exerciseId).remove();

                // change icon under the exercise
                var buttonContainer = document.getElementById('button-container-' + exerciseId);
                if (buttonContainer) {
                    var oldIcon = buttonContainer.querySelector('.fa-xmark');  // "X" icon
                    if (oldIcon) {
                        var newIcon = document.createElement('i');
                        newIcon.setAttribute('onclick', 'addToHard(' + exerciseId + ')');
                        newIcon.setAttribute('title', 'Przypnij zadanie');
                        newIcon.className = 'fa-solid fa-thumbtack';          // "pin" icon
                        buttonContainer.replaceChild(newIcon, oldIcon);
                    }
                }
}
        },
        error: function(xhr, status, error) {
            console.error('Error deleting exercise:', error);
        }
    });
}

function addToHard(exerciseId){
    $.ajax({
        url: `/hard/${exerciseId}`,
        type: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function(response) {
            if (response.status === 'added') {
                console.log('Exercise added to pinned successfully:', exerciseId);

                {/* <a onclick="goToExercise({{ exercise.id }})" class="text-decoration-none cursor-pointer">{{ exercise }}</a> */}
                // add exercise to list of hard exercises
                var ul = document.getElementById('hard-exercises');
                var li = document.createElement('li');
                var link = document.createElement('a');
                link.setAttribute('onclick', 'goToExercise(' + exerciseId + ')');
                link.innerHTML = response.text;
                link.classList.add('text-decoration-none');
                link.classList.add('cursor-pointer');
                li.setAttribute('id', 'hard-exercise-' + exerciseId)
                li.innerHTML = '<i onclick="deleteFromHard(' + exerciseId + ')" title="Usuń z przypiętych zadań" class="fa-solid fa-xmark"></i>';
                li.appendChild(link);
                ul.appendChild(li);

                // change icon under the exercise
                var buttonContainer = document.getElementById('button-container-' + exerciseId);
                if (buttonContainer) {
                    var oldIcon = buttonContainer.querySelector('.fa-thumbtack');  // "pin" icon
                    if (oldIcon) {
                        var newIcon = document.createElement('i');
                        newIcon.setAttribute('onclick', 'deleteFromHard(' + exerciseId + ')');
                        newIcon.setAttribute('title', 'Usuń z przypiętych zadań');
                        newIcon.className = 'fa-solid fa-xmark';          // "X" icon
                        buttonContainer.replaceChild(newIcon, oldIcon);
                    }
                }
            }
        },
        error: function(xhr, status, error) {
            console.error('Error deleting exercise:', error);
        }
    });
}

function goToExercise(exerciseId){
    var exerciseOnPage = document.getElementById('exercise-card-' + exerciseId);
    if (exerciseOnPage) {
        document.getElementById('exercise-card-' + exerciseId).scrollIntoView({behavior: 'smooth', block: 'center'});
    } else {
        window.location.href = '/go-to-exercise/' + exerciseId + '#exercise-card-' + exerciseId;
    }
}

function resetAnswer(exerciseId){
    $.ajax({
        url: `/reset/${exerciseId}`,
        type: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function(response) {
            if (response.status === 'reset') {
                console.log('Info about exercise reseted successfully:', exerciseId);

                clearColorsFromCard(exerciseId);
                updateProgress(response);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error deleting info about answer:', error);
        }
    });
}

function submitAnswer(answerId){
    $.ajax({
        url: `/answer/${answerId}`,
        type: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function(response) {
            var exerciseId = response.exercise_id;
            console.log('Info about exercise updated successfully:', exerciseId);

            var container = document.getElementById('exercise-card-' + exerciseId);
            clearColorsFromCard(exerciseId);

            var card = container.firstElementChild;
            var cardHeader = card.firstElementChild;
            var cardBody = card.lastElementChild;
            var answer = document.getElementById('answer-' + answerId);

            if (response.correct === true){
                card.classList.add('border-success');
                cardHeader.classList.add('background-correct');
                cardBody.classList.add('background-correct');
                answer.classList.add("answer-highlight");
            } else {
                card.classList.add('border-danger');
                cardHeader.classList.add('background-incorrect');
                cardBody.classList.add('background-incorrect');

                // Applying animation if answer is incorrect
                answer.classList.add('wiggle-animation');
                setTimeout(function() {
                    answer.classList.remove('wiggle-animation');
                }, 250);
            }
            updateProgress(response);
        },
        error: function(xhr, status, error) {
            console.error('Error updating info about answer:', error);
        }
    });
}

// update GUI elements with correct percents
function updateProgress(response){
    var totalProgress = response.total_progress;
    var categoryProgress = response.category_progress;
    var categoryId = response.category_id;

    var percentOverCards = document.getElementById('percent-over-cards');
    percentOverCards.innerHTML = categoryProgress + '%';
    var leftSidebarPercent = document.getElementById('left-sidebar-percent-' + categoryId);
    leftSidebarPercent.innerHTML = categoryProgress + '%';
    var progressBar = document.getElementById('progress-bar');
    if (progressBar) {
    progressBar.style.width = totalProgress + '%';
    }
    var percentOverProgressBar = document.getElementById('percent-over-progress-bar');
    if (percentOverProgressBar) {
    percentOverProgressBar.innerHTML = totalProgress + '%';
    }
    var icon = document.getElementById('sidebar-a-' + categoryId).firstElementChild;
    if (categoryProgress === 0) {
        icon.classList = ['fa-solid fa-circle'];
    } else if (categoryProgress < 20) {
        icon.classList = ['fa-solid fa-pencil me-2'];
    } else if (categoryProgress < 40) {
        icon.classList = ['fa-solid fa-pen-fancy'];
    } else if (categoryProgress < 60) {
        icon.classList = ['fa-regular fa-lightbulb'];
    } else if (categoryProgress < 80) {
        icon.classList = ['fa-solid fa-microchip'];
    } else {
        icon.classList = ['fa-solid fa-crown'];
    }
}

function clearColorsFromCard(exerciseId){
    var container = document.getElementById('exercise-card-' + exerciseId);
    var card = container.firstElementChild;
    card.classList.remove('border-success');
    card.classList.remove('border-danger');

    var cardHeader = card.firstElementChild;
    cardHeader.classList.remove('background-correct');
    cardHeader.classList.remove('background-incorrect');

    var cardBody = card.lastElementChild;
    cardBody.classList.remove('background-correct');
    cardBody.classList.remove('background-incorrect');

    var highlitedAnswers = document.querySelectorAll('div#exercise-card-' + exerciseId +  ' .answer-highlight');
    highlitedAnswers.forEach(answer => {
        answer.classList.remove('answer-highlight');
    })

}