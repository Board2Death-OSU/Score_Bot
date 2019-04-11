class StaticController < ApplicationController
  def index
    require 'bundler'
    Bundler.require

    # Authenticate a session with your Service Account
    session = GoogleDrive::Session.from_service_account_key("app/controllers/client_secret.json")

    # Get the spreadsheet by its title
    spreadsheet = session.spreadsheet_by_title("WTS 4 Human Control Record")
    # Get the first worksheet
    worksheet = spreadsheet.worksheets
    rows=worksheet[1].rows
    @terror=rows[15][1]
    @data=[]
    for i in 1..11
        @data.push([rows[i][0],rows[i][1]])
    end
    @data.sort! { |x,y| y[1] <=> x[1] }




  end
end
