'use strict';

angular.module('Agrihack', [])
    // TODO: change this to uirouter (important)
  .config(function ($routeProvider) {

    $routeProvider
      .when('/', {
        templateUrl: 'views/index.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });