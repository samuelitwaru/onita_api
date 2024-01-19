function showModal(option){
    $('#loadingModal').modal(option?'show':'hide')

}

function render(id, template) {
    var container = document.getElementById(id)
    container.innerHTML = template
}

const setTopicOrderUp = (containerId, topicId) => {
    showModal(true)
    axios
    .get(`/api/topics/${topicId}/set-topic-order-up`)
    .then(res=>{
        if (res.status == 200) {
            render(containerId, res.data.template)
        }
        showModal(false)
    })
}

const setTopicOrderDown = (containerId, topicId) => {
    showModal(true)
    axios
    .get(`/api/topics/${topicId}/set-topic-order-down`)
    .then(res=>{
        if (res.status == 200) {
            render(containerId, res.data.template)
        }
        showModal(false)
    })
}

const setSubtopicOrderUp = (containerId, subtopicId) => {
    showModal(true)
    axios
    .get(`/api/subtopics/${subtopicId}/set-subtopic-order-up`)
    .then(res=>{
        if (res.status == 200) {
            render(containerId, res.data.template)
        }
        showModal(false)
    })
}

const setSubtopicOrderDown = (containerId, subtopicId) => {
    showModal(true)
    axios
    .get(`/api/subtopics/${subtopicId}/set-subtopic-order-down`)
    .then(res=>{
        if (res.status == 200) {
            render(containerId, res.data.template)
        }
        showModal(false)
    })
}