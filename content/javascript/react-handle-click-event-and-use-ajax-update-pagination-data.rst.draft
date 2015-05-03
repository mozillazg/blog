var CheckinList = React.createClass({
  loadDataFromServer: function() {
    var page = this.state.page || 1;
    $.ajax({
      url: this.props.url,
      data: {
        'page': page,
        'per_page': this.props.per_page
      },
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handlePageClick: function(event) {
    var page = this.state.page + 1;
    this.setState({page: page}, function() {
        this.loadDataFromServer();
    }.bind(this));
  },

  getInitialState: function() {
    return {data: [], page: 1};
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    var checkinNodes = this.state.data.map(function (checkin) {
      var think = checkin.think.replace('\n', '<br />');
      var bookURL = '/b/name/' + checkin.book_name;
      return (
        <Checkin checkin={checkin} key={checkin.id}>
          #打卡 <a href={bookURL}>《{checkin.book_name}》</a> {think}
        </Checkin>
      )
    });
    return (
      )
    });
    return (
      <div>
        {checkinNodes}
        <div className="pagenation">
            <a onClick={this.handlePageClick}>next</a>
        </div>
      </div>
    );
  }
});