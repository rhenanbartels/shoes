let currentPage = 1
let isCurrentlyLoadingNextPage = false
let hasMorePhotosToLoad = true
let isShowingSearch = false
let searchParameter
const IMAGE_CONTAINER_BOOTSTRAP_CLASS = 'col-4' // multiple of 12
const endlessFooterAuxiliaryElement = document.querySelector('.footer-endless-scroll')
const loadingElement = document.querySelector('#loading')
const noImagesToShow = document.querySelector('#no-images')
const searchInputText = document.getElementById('search_input_text')
const searchInputDate = document.getElementById('search_input_date')
// DOM element to display the images
let $images = document.getElementById('images')

const init = () => {
    fetchImages()
    initEndlessScrollEvent()
    initSearchEvents()
}

const fetchImages = () => {
    showLoading()
    let API_URL = '/api/feed?page=' + currentPage
    if (isShowingSearch) {
        API_URL = '/api/search?' + searchParameter + '&page=' + currentPage
    }
    if (currentPage === 1) {
        hasMorePhotosToLoad = true
    }
    fetch(API_URL).then(response => {
        response.json().then(data => {
            hideLoading()
            hideMessageNoImagesToShow()
            console.log(data)
            fillImages(data)
            isCurrentlyLoadingNextPage = false
            if (data.length === 0) {
                hasMorePhotosToLoad = false
                if (currentPage === 1) {
                    showMessageNoImagesToShow()
                }
            }
        })
    })
}

const emptyImages = () => {
    // empty its contents
    while ($images.firstChild) {
        $images.removeChild($images.firstChild)
    }
}

const fillImages = images => {
    // for each image
    images.map(image => {
        let imageUrl = image.image_aws_url

        // create an <img>
        let $image = document.createElement('img')
        $image.setAttribute('src', imageUrl)

        // create an <a>
        let $hyperlink = document.createElement('a')
        $hyperlink.setAttribute('href', imageUrl)
        $hyperlink.setAttribute('target', '_blank')
        // append the image to the hyperlink
        $hyperlink.appendChild($image)

        // create a <div> for details
        let $details = document.createElement('div')
        $details.setAttribute('class', 'details')
        // username
        let $username = document.createElement('a')
        $username.setAttribute('class', 'username')
        $username.setAttribute('href', 'http://instagram.com/' + image.user.username)
        $username.setAttribute('target', '_blank')
        $username.textContent = '@' + image.user.username
        $details.appendChild($username)
        // instagram link
        if (image.source === 'feed') {
            let $br = document.createElement('br')
            $details.appendChild($br)
            let $instagramLink = document.createElement('a')
            $instagramLink.setAttribute('href', 'http://instagram.com/p/' + image.code)
            $instagramLink.setAttribute('target', '_blank')
            $instagramLink.textContent = 'Ver no Instagram'
            $details.appendChild($instagramLink)
        }
        // likes & comments
        if (image.comment_count || image.like_count) {
            let $likesComments = document.createElement('div')
            $likesComments.textContent = '🖤 ' + image.like_count + ' / 💬 ' + image.comment_count
            $details.appendChild($likesComments)
        } else {
            let $storyComments = document.createElement('div')
            $storyComments.textContent = '(story)'
            $details.appendChild($storyComments)
        }

        // create a container
        let $imageContainer = document.createElement('div')
        $imageContainer.setAttribute('class', IMAGE_CONTAINER_BOOTSTRAP_CLASS)
        // append the hyperlink and the image to the container
        $imageContainer.appendChild($hyperlink)
        // append the details
        $imageContainer.appendChild($details)
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

const showLoading = () => {
    loadingElement.className = ''
}

const hideLoading = () => {
    loadingElement.className = 'hidden'
}

const showMessageNoImagesToShow = () => {
    noImagesToShow.className = ''
}

const hideMessageNoImagesToShow = () => {
    noImagesToShow.className = 'hidden'
}

const initSearchEvents = () => {
    document.getElementById('search_option').onchange = changeSearchOption
    document.getElementById('do_search').onclick = doSearch
    document.getElementById('clear_search').onclick = clearSearch
}

const changeSearchOption = e => {
    let searchOption = document.getElementById('search_option').value
    if (searchOption === 'date') {
        searchInputDate.className = ''
        searchInputText.className = 'hidden'
    } else {
        searchInputDate.className = 'hidden'
        searchInputText.className = ''
    }
}

const doSearch = e => {
    let searchOption = document.getElementById('search_option').value
    if (searchOption === 'date') {
        let startDate = document.querySelector('#start_date').value
        let endDate = document.querySelector('#end_date').value
        if (startDate === '' || endDate === '') {
            alert('É preciso escolher uma data inicial e final para realizar a busca.')
            return false
        }
        callSearchAPI('start_date=' + getUnixDate(startDate) + '&end_date=' + getUnixDate(endDate))
    } else {
        let searchValue = searchInputText.value
        
        // treat empty values
        if (searchValue === '') {
            alert('É preciso digitar um valor para fazer a busca.')
            return false
        }

        // specific treatments
        if (searchOption === 'username') {
            // remove @
            searchValue = searchValue.replace('@', '')
        } else if (searchOption === 'hashtags') {
            searchValue = searchValue.replace(/#/g, '').split(' ').map(t => '%23' + t).join('|')
        }
        callSearchAPI(searchOption + '=' + searchValue)
    }
    e.preventDefault()
    return false
}

const getUnixDate = dateString => {
    if (dateString === '') {
        return null
    }
    let dateArray = dateString.split('-').map(s => parseInt(s, 10))
    let dateObj = new Date(dateArray[0], dateArray[1] - 1, dateArray[2])
    return (+dateObj)/1000
}

const callSearchAPI = endpoint => {
    console.log(endpoint)
    emptyImages()
    isShowingSearch = true
    searchParameter = endpoint
    currentPage = 1
    fetchImages()
}

const clearSearch = e => {
    searchInputText.value = ''
    emptyImages()
    isShowingSearch = false
    searchParameter = null
    currentPage = 1
    fetchImages()
    e.preventDefault()
    return false
}

init()
