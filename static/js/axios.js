const BASE_URL = '127.0.0.1:8000/api';

function render(id, template) {
    var container = document.getElementById(id)
    container.innerHTML = template
}

const setTopicOrderUp = (containerId, topicId) => {
    axios
    .get(`/api/topics/${topicId}/set-topic-order-up`)
    .then(res=>{
        if (res.status == 200) {
            render(containerId, res.data.template)
        }
    })
}

const setTopicOrderDown = (containerId, topicId) => {
    axios
    .get(`/api/topics/${topicId}/set-topic-order-down`)
    .then(res=>{
        if (res.status == 200) {
            render(containerId, res.data.template)
        }
    })
}