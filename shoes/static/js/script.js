let currentPage = 1
const $nextButton = document.getElementById('next_page')
const $previousButton = document.getElementById('previous_page')

const init = () => {
    updatePreviousButtonStatus()
    fetchImages()
    paginateButtonsEvents()
}

const fetchImages = () => {
    fetch('/api/feed?page=' + currentPage).then(response => {
        response.json().then(data => {
            console.log(data)
            updatePreviousButtonStatus()
            updateNextButtonStatus(data)
            fillImages(data)
        })
    })
}

const fillImages = images => {
    // DOM element to display the images
    let $images = document.getElementById('images')

    // empty its contents
    while ($images.firstChild) {
        $images.removeChild($images.firstChild)
    }

    // for each image
    images.map(image => {
        // create an <img>
        let $image = document.createElement('img')
        $image.setAttribute('src', 'data:image/jpg;base64,' + image.image_base64)
        // create a container
        let $imageContainer = document.createElement('div')
        $imageContainer.setAttribute('class', 'col-2')
        // append the image to the container
        $imageContainer.appendChild($image)
        // append it to DOM
        $images.appendChild($imageContainer)
    })
}

const paginateButtonsEvents = () => {
    $nextButton.onclick = onNextPage
    $previousButton.onclick = onPreviousPage
}

const onNextPage = e => {
    console.log('next page click')
    currentPage++
    fetchImages()
}

const onPreviousPage = e => {
    console.log('previous page click')
    currentPage--
    fetchImages()
}

const updatePreviousButtonStatus = () => {
    if (currentPage === 1) {
        $previousButton.disabled = true
    } else {
        $previousButton.disabled = false
    }
}

const updateNextButtonStatus = data => {
    if (data.length === 0) {
        $nextButton.disabled = true
    } else {
        $nextButton.disabled = false
    }
}

init()