/**
 * The main controller for the app. The controller:
 * - retrieves and persists the model via the todoStorage service
 * - exposes the model to the template and provides event handlers
 */
angular.module('siteApp')
    .controller('RegisterCtrl', [ '$scope',  '$http', '$location', function ($scope, $http, $location) {

        $scope.formData = {};
        $scope.showSuccess = false;
        $scope.showError = false;
        $scope.messge = "";

        $scope.steps = [
            'Шаг 1: Сайт',
            'Шаг 2: Контакты'
        ];
        $scope.selection = $scope.steps[0];

        $scope.getCurrentStepIndex = function () {
            // Get the index of the current step given selection
            return _.indexOf($scope.steps, $scope.selection);
        };

        // Go to a defined step index
        $scope.goToStep = function (index) {
            if (!_.isUndefined($scope.steps[index])) {
                $scope.selection = $scope.steps[index];
            }
        };

        $scope.hasNextStep = function () {
            var stepIndex = $scope.getCurrentStepIndex();
            var nextStep = stepIndex + 1;
            // Return true if there is a next step, false if not
            return !_.isUndefined($scope.steps[nextStep]);
        };

        $scope.hasPreviousStep = function () {
            var stepIndex = $scope.getCurrentStepIndex();
            var previousStep = stepIndex - 1;
            // Return true if there is a next step, false if not
            return !_.isUndefined($scope.steps[previousStep]);
        };

        $scope.incrementStep = function () {
            if ($scope.hasNextStep()) {
                var stepIndex = $scope.getCurrentStepIndex();
                var nextStep = stepIndex + 1;
                $scope.selection = $scope.steps[nextStep];
            }
        };

        $scope.decrementStep = function () {
            if ($scope.hasPreviousStep()) {
                var stepIndex = $scope.getCurrentStepIndex();
                var previousStep = stepIndex - 1;
                $scope.selection = $scope.steps[previousStep];
            }
        };

        $scope.submitForm = function(form){

            if(form.$invalid) return;

            $http.post('/api/publisher/v1/publisher_order/', $scope.formData)
		    .success(function(data, status, headers, config) {

			    console.log("Success",data);
                    if(status == 201){
                        $scope.formData = {};
                        $scope.showSuccess = true;
                        $scope.message = "Успех! Спасибо большое за оставленную заявку.\n Мы свяжемся с Вами в ближайщее веремя";
                    } else{
                        $scope.showError = true;
                        $scope.message = "Ошибка! Произошла ошибка при обработке Вашей заявки";
                    }



		    }).error(function(response){
                    console.log(response);
                    $scope.showError = true;
                    $scope.message = "Ошибка! Произошла ошибка соединения. Попробуйте позже повторить запрос.";
            });



        }
    }

    ]);