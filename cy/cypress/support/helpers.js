export class UrlHelper {
  constructor(hostname, scheme, port) {
    this.hostname = hostname;
    this.port = port;  
    this.scheme = scheme !== undefined ? scheme : 'http://';
    if (this.hostname == undefined) {
      throw 'undefined hostname';
    }
    this.url = this.scheme + this.hostname + ( this.port == undefined ? '' : ':' + this.port );
  }
  getFullUrl(query) {
    return (
      this.url +
      (query !== undefined ? (query.charAt(0) === '/' ? '' : '/') + query : '')
    );
  }
}

export class QueryHelper {
  constructor(prefix) {
    this.prefix = prefix;
  }

  getQuery(query) {
    return this.prefix + (query !== undefined ? query : '');
  }
}
