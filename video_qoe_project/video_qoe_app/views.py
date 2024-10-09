from django.shortcuts import render, redirect
from .models import QoeVideo, Respondent, ValidationVideo
from .forms import CreateQuestionnaireForm
from django.contrib import messages
import random


# Define GLOBAL variables
# respondent_id = 0
# playlist = {}
# validation_video = ""


def get_random_videos_id_from_model():
    random_video_id = random.sample(range(1, 219), 9)  # range(2, 7), 4 //range(1,3) means create numbers from 1 to 2, 3 won't be included
    return random_video_id


def fetch_videos_from_model():
    random_video_ids = get_random_videos_id_from_model()
    # print(type(random_video_ids))
    video_playlist = {}  # Dict
    video_path_list = []  # List
    video_id_list = []  # List
    for random_id in random_video_ids:
        # print("fetch_videos_from_model - this is random number", random_id)
        try:
            video_obj = QoeVideo.objects.get(video_id=random_id)
            video_path = video_obj.video_file_path
            video_id_num = video_obj.video_id
            # print(type(video_obj))
            # print(type(video_id_num))
        except QoeVideo.DoesNotExist:
            video_path = None
            video_id_num = None

        video_path_list.append(video_path)
        video_id_list.append(video_id_num)
        # print("fetch_videos_from_model - this is path list", video_path_list)
        # print("fetch_videos_from_model - this is id_num list", video_id_list)

    for i in range(len(video_id_list)):
        video_playlist[video_id_list[i]] = video_path_list[i]
        # print("fetch_videos_from_model - this is dict playlist", video_playlist)
    return video_playlist


def fetch_validation_videos():
    random_validation_video_id = random.randint(2, 5)

    try:
        validation_video_obj = ValidationVideo.objects.get(validation_video_id=random_validation_video_id)
        validation_video_path = validation_video_obj.validation_video_file_path
    except ValidationVideo.DoesNotExist:
        validation_video_path = None

    return validation_video_path


# Create your views here.
def welcome_page(request):
    try:
        del request.session["playlist_dict"]
        del request.session["validation_video"]
        del request.session["respondent_id"]
    except KeyError:
        print("Before Pass in welcome_page")
        pass
    return render(request, 'video_qoe_app/welcome.html')  # specify template name


def questionnaire_page(request):
    playlist = fetch_videos_from_model()
    validation_video = fetch_validation_videos()

    request.session["playlist_dict"] = playlist
    request.session["validation_video"] = validation_video

    form = CreateQuestionnaireForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            respondent_age_range = form.cleaned_data['age_range']  # pass cleaned values from form to a variable
            respondent_gender = form.cleaned_data['gender']
            create_respondent = Respondent(age_range=respondent_age_range, gender=respondent_gender)
            create_respondent.save()

            # Try to get ID of newly saved respondent
            try:
                respondent_id = create_respondent.respondent_id
                request.session["respondent_id"] = respondent_id
            except create_respondent.DoesNotExist:
                respondent_id = None
            print("This is resp ID", respondent_id)

            if respondent_id is not None and "respondent_id" in request.session:
                return redirect("survey", param=respondent_id)
            else:
                form = CreateQuestionnaireForm()
                context = {'form': form}
                return render(request, 'video_qoe_app/questionnaire.html', context)
    return render(request, 'video_qoe_app/questionnaire.html', {"form": form})  ##use name of url here after testing


def survey_page(request, param):
    # respondent_details = 0
    try:
        playlist = request.session["playlist_dict"]
        validation_video = request.session["validation_video"]

        print("param value ", param)
        print("at begining of survey_page", playlist)
        print("at begining of survey_page", validation_video)
    except KeyError:
        print("Inside KeyError in survey_page")
        playlist = {}

    try:
        respondent_details = Respondent.objects.get(
            respondent_id=param)  ##need to look at respondent_details, maybe declare the variable
        print("inside try in survey_page", respondent_details)
    except Respondent.DoesNotExist:
        print("inside catch exception in survey_page", respondent_details)
        # print(respondent_details)
        return redirect("welcome")

    if len(playlist) == 0:
        messages.error(request, 'Something went wrong. Please kindly retake the survey')
        return redirect("welcome")

    if request.method == 'POST':
        print(playlist)
        if request.POST.get('submit_rating'):  # submit button
            for key, value in playlist.items():
                try:
                    new_rated_video = QoeVideo.objects.get(video_id=key)
                except QoeVideo.DoesNotExist:
                    new_rated_video = None
                    print("Video should be empty", new_rated_video)

                new_rating_perception = request.POST.get('qoe_rating_one_' + str(key))
                new_rating_value = request.POST.get('qoe_rating_two_' + str(key))
                new_validation_video_resp = request.POST.get('validation_question')

                if new_rated_video is None or new_rating_perception is None or new_rating_value is None or new_validation_video_resp is None:
                #if not all(v is None for v in [new_rating_perception, new_rating_value, new_validation_video_resp, new_rated_video]):
                    messages.error(request, 'Something went wrong. Please kindly retake the survey')
                    return redirect("welcome")
                else:
                    respondent_details.qoerating_set.create(qoe_rating_value=new_rating_value,
                                                            qoe_rating_perception=new_rating_perception,
                                                            video=new_rated_video,
                                                            respondent_validation_video_anwer=new_validation_video_resp,
                                                            validation_video_path=validation_video)

        return redirect("end", resp_param=respondent_details.respondent_id)

    print("at end of survey_page",
          playlist)  # get the key of playlist dict and passs it to qoe_rating_one and two keys, also use the key to get the video obj
    print("at end of survey_page", validation_video)
    context = {'playlist': playlist,
               'validation_video': validation_video,
               'respondent_details': respondent_details.respondent_id}
    # 'error_message': error_message}
    return render(request, 'video_qoe_app/survey.html', context)


def bye_page(request):
    return render(request, 'video_qoe_app/bye.html')


def end_page(request, resp_param):
    # global respondent_id
    # current_respondent_id = request.session.get("respondent_id")
    if request.POST.get("more_rating"):
        rate_more_response = request.POST.get("more_rating")
        if rate_more_response == "Yes":
            session_respondent_id = request.session["respondent_id"]
            try:
                del request.session["playlist_dict"]
                del request.session["validation_video"]
            except KeyError:
                print("cant delete playlist and val video sessions")
                pass
            print("respondent_id inside end with Yes response", session_respondent_id)
            return redirect("ratemore", rate_param=resp_param)
            # rmb to delete old videos in session
        else:
            try:
                print("Inside Try end_page", request.session["respondent_id"])
                del request.session["respondent_id"]
            except KeyError:
                print("Before Pass in end_page", request.session["respondent_id"])
                pass
            return redirect("bye")
    return render(request, 'video_qoe_app/end.html', {"resp_param": resp_param})


def ratemore_page(request, rate_param):
    playlist = fetch_videos_from_model()
    validation_video = fetch_validation_videos()

    request.session["playlist_dict"] = playlist
    request.session["validation_video"] = validation_video
    return render(request, 'video_qoe_app/ratemore.html', {"rate_param": rate_param})

# https://stackoverflow.com/questions/22976662/return-primary-key-after-saving-to-a-model-in-django
# https://stackoverflow.com/questions/5130639/django-setting-a-session-and-getting-session-key-in-same-view
# https://stackoverflow.com/questions/46267296/how-do-i-pass-a-dictionary-from-one-view-to-another-in-django-using-session
# https://code.djangoproject.com/wiki/NewbieMistakes
# https://stackoverflow.com/questions/57177446/random-number-changes-before-making-a-post-request
# https://stackoverflow.com/questions/51155947/django-redirect-to-another-view-with-context
# https://stackoverflow.com/questions/14465993/how-to-set-and-get-session-in-django
# https://stackoverflow.com/questions/76644005/request-session-clear-vs-request-session-flush-in-django
# https://stackoverflow.com/questions/59519378/what-is-the-difference-between-using-the-request-session-flush-and-simply-usin#:~:text=flush()%20delete%20the%20record,session_data%20on%20the%20django_session%20table.
# https://stackoverflow.com/questions/44478979/html5-video-wrong-height-in-flexbox
# https://www.youtube.com/watch?v=PtQiiknWUcI
# https://forum.jquery.com/portal/en/community/topic/check-if-al-radio-buttons-are-checked
# https://simpleisbetterthancomplex.com/questions/2017/03/17/getting-form-data-to-appear-in-url-and-for-use-in-the-next-view.html
# https://simpleisbetterthancomplex.com/tutorial/2021/06/27/how-to-start-a-production-ready-django-project.html
# https://jsfiddle.net/yxpc9qr9/
# https://www.codexworld.com/how-to/check-if-radio-button-in-group-checked-jquery/
# https://stackoverflow.com/questions/71013553/show-hide-html-sections-on-button-click
# https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code
# https://stackoverflow.com/questions/44948027/passing-id-from-createview-to-another-function-after-creating-the-object
# https://stackoverflow.com/questions/70833034/heroku-django-request-post-giving-wrong-values
# https://stackoverflow.com/questions/71459136/pg-restore-error-unrecognized-data-block-type-0-while-searching-archive-whil/71852548#71852548
# https://superuser.com/questions/1671646/changing-default-user-for-postgresql-on-windows-10
# https://www.youtube.com/watch?v=ftpepZo9GSI
# https://www.youtube.com/watch?v=CkYvpKZyEqI
# https://www.youtube.com/watch?v=IiUYyZo2gTk
# https://www.youtube.com/watch?v=PtQiiknWUcI
# https://stackoverflow.com/questions/2741493/detect-when-an-html5-video-finishes
# https://stackoverflow.com/questions/3221561/eliminate-flash-of-unstyled-content