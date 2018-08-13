let currentPage = 1
let isCurrentlyLoadingNextPage = false
let hasMorePhotosToLoad = true
const IMAGE_CONTAINER_BOOTSTRAP_CLASS = 'col-4' // multiple of 12
const endlessFooterAuxiliaryElement = document.querySelector('.footer-endless-scroll')

const init = () => {
    fetchImages()
    initEndlessScrollEvent()
}

const fetchImages = () => {
    fetch('/api/feed?page=' + currentPage).then(response => {
        response.json().then(data => {
            console.log(data)
            fillImages(data)
            isCurrentlyLoadingNextPage = false
            if (data.length === 0) {
                hasMorePhotosToLoad = false
            }
        })
    })
}

const fillImages = images => {
    // DOM element to display the images
    let $images = document.getElementById('images')

    // empty its contents
    // while ($images.firstChild) {
    //     $images.removeChild($images.firstChild)
    // }

    // for each image
    images.map(image => {
        let imageUrl = 'data:image/jpg;base64,' + image.image_base64
        // create an <img>
        let $image = document.createElement('img')
        $image.setAttribute('src', imageUrl)
        // create an <a>
        let $hyperlink = document.createElement('a')
        $hyperlink.setAttribute('href', imageUrl)
        $hyperlink.setAttribute('target', '_blank')
        // append the image to the hyperlink
        $hyperlink.appendChild($image)
        // create a container
        let $imageContainer = document.createElement('div')
        $imageContainer.setAttribute('class', IMAGE_CONTAINER_BOOTSTRAP_CLASS)
        // append the hyperlink and the image to the container
        $imageContainer.appendChild($hyperlink)
        // append it to DOM
        $images.appendChild($imageContainer)
    })
}

const onNextPage = e => {
    currentPage++
    console.log('Loading page', currentPage)
    fetchImages()
}

const initEndlessScrollEvent = () => {
    window.onscroll = e => {
        let endlessFooterPosition = endlessFooterAuxiliaryElement.getBoundingClientRect()
        if (!isCurrentlyLoadingNextPage && hasMorePhotosToLoad) {
            if (endlessFooterPosition.y - window.pageYOffset < 300) {
                isCurrentlyLoadingNextPage = true
                onNextPage()
            }
        }
    }
}

init()