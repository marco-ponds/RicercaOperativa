class TestController < ApplicationController

    def prova
        render json: {:message => "YO"}
    end

    def prova_due
        render json: {:message => params[:prova]}
    end

end

