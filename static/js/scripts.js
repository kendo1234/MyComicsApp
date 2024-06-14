$(document).ready(function() {
    // Handle search form submission
    $('#searchForm').on('submit', function(e) {
        e.preventDefault();
        let searchType = $('#searchType').val();
        let searchValue = $('#searchValue').val();

        $.ajax({
            url: `/comics/${searchType}/${searchValue}`,
            method: 'GET',
            success: function(data) {
                displayResults(data);
            },
            error: function() {
                $('#results').html('<div class="alert alert-danger">No comics found.</div>');
            }
        });
    });

    // Handle add form submission
    $('#addForm').on('submit', function(e) {
        e.preventDefault();
        let newComic = {
            Title: $('#title').val(),
            Volume: $('#volume').val(),
            Writer: $('#writer').val(),
            Artist: $('#artist').val()
        };

        $.ajax({
            url: '/comics',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(newComic),
            success: function(data) {
                $('#results').html('<div class="alert alert-success">Comic added successfully!</div>');
                $('#addForm')[0].reset();
            },
            error: function() {
                $('#results').html('<div class="alert alert-danger">Failed to add comic.</div>');
            }
        });
    });

    // Handle delete form submission
    $('#deleteForm').on('submit', function(e) {
        e.preventDefault();
        let title = $('#deleteTitle').val().trim().toLowerCase();

        $.ajax({
            url: `/comics/title/${title}`,
            method: 'DELETE',
            success: function(data) {
                $('#results').html('<div class="alert alert-success">Comic deleted successfully!</div>');
                $('#deleteForm')[0].reset();
            },
            error: function() {
                $('#results').html('<div class="alert alert-danger">Failed to delete comic.</div>');
            }
        });
    });

    // Function to display search results
    function displayResults(data) {
        if (data.length === 0) {
            $('#results').html('<div class="alert alert-warning">No comics found.</div>');
            return;
        }

        let html = '<div class="list-group">';
        data.forEach(comic => {
            html += `<div class="list-group-item">
                        <h5>${comic.Title}</h5>
                        <p>Volume: ${comic.Volume}</p>
                        <p>Writer: ${comic.Writer}</p>
                        <p>Artist: ${comic.Artist}</p>
                    </div>`;
        });
        html += '</div>';
        $('#results').html(html);
    }
});
