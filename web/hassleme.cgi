#!/usr/bin/perl -w -I../perllib -I../commonlib/perllib
#
# hassleme.cgi:
# Website for hassleme.
#
# Copyright (c) 2005 Chris Lightfoot. All rights reserved.
# Email: chris@ex-parrot.com; WWW: http://www.ex-parrot.com/~chris/
#

use strict;

use CGI qw(-no_xhtml);
use mySociety::CGIFast;
use Data::Dumper;
use HTML::Entities qw(encode_entities);
use IO::Pipe;
use HTML::Entities;
use Net::DNS;
use FindBin;
use Path::Tiny;

use Hassle;
use mySociety::Config;
use Template;

my $tt = Template->new(
    INCLUDE_PATH => '../templates',
);

BEGIN {
    mySociety::Config::set_file("$FindBin::Bin/../conf/general");
}

sub _ {
    # TODO - this is the function that will become the stub function for il18n and l10n
    return @_;
}

sub hassle_header {
    my ($q, $title) = @_;
    my $fn = lc($q->param('fn'));
    $fn ||= 'home';
    my $header_title = "HassleMe";
    if ($title) {
        $header_title .= " - $title";
    }
    print
        $q->header(-type => 'text/html; charset=utf-8'),
        $q->start_html(
            -title => $header_title,
            -style => { -src => [
                '/hassleme.css',
                '//fonts.googleapis.com/css?family=Source+Sans+Pro:400,600',
                '/assets/css/banner.css',
            ] },
        );

    my $staging = mySociety::Config::get('HM_STAGING') ? 1 : 0;
    if ($staging) {
        print $q->div( { style=>'background-color: red; text-align: center; padding: 1em; color: white;' },
            "This is a test site for developers only, you want",
            $q->a({href=>'http://www.hassleme.co.uk'}, "www.hassleme.co.uk")
        );
    }

print <<EOF;
<div class="retirement-banner retirement-banner--hassleme">
  <div class="retirement-banner__inner">
    <a class="retirement-banner__logo" href="https://www.mysociety.org/">mySociety</a>
    <p class="retirement-banner__description">
        HassleMe is changing!
    </p>
    <p class="retirement-banner__description">
        During the transition period until 9th March, creation of new hassles is disabled.
        But you can still browse existing ones.
        <a class="retirement-banner__more" href="/T/TCs">Find out more!</a></p>
  </div>
</div>
EOF

    print $q->h1($q->a({href=>'/'},"HassleMe"),
#                 $q->span({-id=>'betaTest'},
#                        'Beta Test'),
                 $q->span({-id=>'slogan'},
                          _("Because sometimes in life,<br>you just need to be nagged...")),
                 );
    print _('<div id="w"><div id="content">');
    if ($title) {
        print $q->h2($title);
    }
}

sub hassle_intro {
    print <<EOF;
<div id="intro">
<p><strong>Not eating enough fruit?</strong> Forgot to feed the fish again?
Need a little help keeping your New Year's resolutions? <br>Tell us what to
hassle you about, and we'll nag you via email at <strong>semi-unpredictable intervals</strong>.
<br>HassleMe is unique because you <strong>never quite know</strong> when your
reminder will come along.</p>
</div>
EOF
}

sub hassle_form {
    my ($q) = @_;

    $q->delete('fn');

    print $q->div({id=>'createHassleBox'},
              $q->h2('Set up a hassle now!'),
              $q->p('Signing up for hassles is not currently available.')
    );

    hassle_recent($q);
}

sub hassle_recent {
    my ($q) = @_;

        print <<EOF;
<div id="exampleHasslesBox">
<h2>Example Hassles</h2>
<ul>
<li><b>Go to the gym</b> roughly every 4 days</li>
<li><b>Write an entry in my diary</b> roughly every 3 days</li>
<li><b>Call your mother</b> roughly every 7 days</li>
<li><b>Go to the theatre</b> roughly every 21 days</li>
<li><b>Spend 5 hours doing something for <a href="http://www.mysociety.org/helpus/">mySociety</a></b> roughly every 28 days</li>
<li><b>Practice the piano</b> roughly every 3 days</li>
<li><b>Go for a walk in the park</b> roughly every 10 days</li>
</ul>
<p align="right"><a href="/hassles">Read lots of hassles</a></p>
<!--
<h2>Recently on HassleMe</h2>
<ul>People asked to be sent these hassles:
<li><a href="/hassleme.cgi?fn=home&f=1&freq=14&what=Go+to+the+theatre&public=false&email=">Go to the theatre every 14 days</a></li>
<li><a href="/hassleme.cgi?fn=home&f=1&freq=4&what=Go+to+the+gym&public=false&email=">Go to the gym every 4 days</a></li>
<li><a href="/hassleme.cgi?fn=home&f=1&freq=7&what=Call+your+mother&public=false&email=">Call your mother every 7 days</a></li>
</ul>
-->
</div>

<!--
<div id="news">
<h2>Upcoming Features</h2>
<ul>
<li>Get hassled via <acronym title="Instant Messaging services like AIM, ICQ, MSN Messenger, Jabber, Google Talk">IM</acronym>.</li>
<li>Specify time in hours, days, weeks and months.</li>
<li>Translation into other languages.</li>
<li>Other cool stuff!</li>
</ul>
</div>
-->

EOF

}

sub hassle_footer {
    my ($q) = @_;
    print <<EOF;

</div></div>

<p id="footer">
<a href="/faq">FAQ</a> |
<a href="/privacy">Privacy and cookies</a> |
Derived from <a href="http://www.mysociety.org/2005/03/17/the-management-power-of-evil/">Hasslebot</a>, a
<a href="http://www.mysociety.org/">mySociety</a> tool that reminds us to post
things on our <a href="http://www.mysociety.org/blog/">blog</a><br>
</p>

EOF

    if ($ENV{'SERVER_NAME'} eq 'www.hassleme.co.uk') {
        print <<EOF;
           <!-- Google Analytics -->
           <script type="text/javascript">

             var _gaq = _gaq || [];
             _gaq.push(['_setAccount', 'UA-660910-8']);
             _gaq.push (['_gat._anonymizeIp']);
             _gaq.push(['_trackPageview']);

             (function() {
               var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
               ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
               var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
             })();

           </script>
            <!-- End Google Analytics Tag -->
EOF
    }

    print $q->end_html();
}

while (my $q = new mySociety::CGIFast()) {
#    $q->autoEscape(0);
    my $fn = lc($q->param('fn'));
    $fn ||= 'home';
    my %fns = map { $_ => 1 } qw(home confirm unsubscribe faq hassles privacy terms);
    $fn = 'home' if (!exists($fns{$fn}));

    if ($fn eq 'home') {
        hassle_header($q);
        hassle_intro();
        hassle_form($q);
    } elsif ($fn eq 'confirm') {
        my $token = $q->param('token');
        my $id = check_token($token);
        if (defined($id)) {
            dbh()->do('update recipient set confirmed = true where id = ?',
                        {}, $id);
            dbh()->commit();
            hassle_header($q,'Confirmed!');
            print <<EOF;
<div id="donatemessage">
<p>
Well done - we'll now hassle you as per your request.
</p>
<p>
If you like this service, <a href="http://www.mysociety.org/donate/">please donate</a>!
</p>
<p><a href="http://www.mysociety.org/donate/"><img src="/waving.jpg" alt=""></a></p>
<p>
We're a registered non-profit running in the UK, and we need your help
to run services like this. For more info see
<a href="http://www.mysociety.org">http://www.mysociety.org</a>.
</p>
</div>
EOF
        } else {
                hassle_header($q,'Oops!');
                print $q->p({-id=>'errors'},
                            "Sorry. We couldn't understand the link you've followed."
                            );
        }
    } elsif ($fn eq 'unsubscribe') {
        my $token = $q->param('token');
        my $id = check_token($token);
        if (defined($id)) {
            dbh()->do('delete from recipient where id = ?',
                        {}, $id);
            dbh()->commit();
            hassle_header($q,'Stopped!');
            print $q->div({-id=>'donatemessage'},
                    <<EOF
                    <p>Thanks! We'll stop hassling you about that, starting now.</p>

                    <p>If HassleMe has been useful to you, please donate to the non-profit
                    which runs it.</p>

                    <p><a href="http://www.mysociety.org/donate">Donate</a>.</p>
EOF
                );
        } else {
            hassle_header($q,'Oops!');
            print $q->p({-id=>'errors'},
                    "Sorry. We couldn't understand the link you've followed."
                );
        }
    } elsif ($fn eq 'hassles') {
        my $longest = $q->param('longest') ? 1 : 0;

        if ($longest) {
            hassle_header($q, 'Longest hassles');
        } else {
            hassle_header($q,'Publicly visible hassles');
        }

        if ($longest) {
            print <<EOF;
            <div id="message">
                <p>Below are 100 things which users of HassleMe have asked to be unpredictably
                reminded of. You may like to see instead <a href="/hassles">100 random hassles</a>.
            </div>
EOF
            } else {
            print <<EOF;
            <div id="message">
                <p>Below are 100 things which users of HassleMe have asked to be unpredictably
                reminded of. <a href="/hassles">Reload the page</a> for another 100.
                <strong>Warning!</strong> There may be strong language within hassles, that's just the way people are. Don't read them if that bothers you.</p>
            </div>
EOF
        }
        my $sth;
        if ($longest) {
            $sth = dbh()->prepare("select what, frequency, whencreated from hassle, recipient where recipient.hassle_id = hassle.id and public and confirmed order by frequency desc limit 100");
        } else {
            $sth = dbh()->prepare("select what, frequency, whencreated from hassle, recipient where recipient.hassle_id = hassle.id and public and confirmed order by random() limit 100");
        }

        $sth->execute;
        print '<table border="0" width="100%"><tr><td width="50%">';
        my $odd = 0;
        my $x = "<b>foo</b>";
        while (my @row = $sth->fetchrow_array) {
            my ($what, $frequency, $whencreated) = @row;
            print "<b>" . CGI::escapeHTML($what) . "</b> roughly every " . $frequency . " " . ($frequency > 1 ? "days" : "day");
            print "</td></tr><tr><td width=\"50%\">" if ($odd);
            print "</td><td width=\"50%\">" if (!$odd);
            print "\n";
            $odd = 1 - $odd;
        }
        print '</td></tr></table>';
        if ($longest) {
            print <<EOF;
            <div id="message">
                <p>You may like to see <a href="/hassles">100 random hassles</a>.
            </div>
EOF
        } else {
        print <<EOF;
            <div id="message">
                <p><a href="/hassles">Reload the page</a> for another 100, or
                see the <a href="/hassles/longest">longest hassles</a>.
                </p>
            </div>
EOF
        }
    } elsif ($fn eq 'faq') {
                hassle_header($q,'Frequently Asked Questions');
                print <<EOF;
<dl>

<dt>What is this site?</dt>

<dd>HassleMe is a tool which nags you. It nags you via email about things
you know you should be doing, but which you'll forget.</dd>

<dt>How often does it nag?</dt>

<dd>You set up a rough frequency, but it actually nags you at random times
within certain parameters. It keeps you on your toes.</dd>

<dt>Why do you think it'll work?</dt>

<dd>mySociety's developer <a href="http://www.ex-parrot.com/~chris/">Chris
Lightfoot</a> built a little program called
<a href="http://www.mysociety.org/?p=16">Hasslebot</a>, to encourage the
developers and volunteers at mySociety to post frequently to our blog, letting
people know what mySociety was up to. Despite the fact that it shouldn't work,
it did.</dd>

<dt>How do I cancel a hassle?</dt>

<dd>Every time we hassle you there will be a link that you can
click to cancel it.</dd>

<dt>If I give you my email address, will you send me spam?<dt>

<dd><b>No!</b> We will only ever send you email when someone
(hopefully you) uses this website to set up a hassle (i.e. we'll send
you a "please confirm this hassle" email), and to carry out the actual
hassling (i.e. the regular nagging emails telling you to go the gym,
write to your mother, etc.). We won't sell your email address to
anyone, and we won't send you spam &mdash; ever.</dd>

<dt>Who are you?</dt>

<dd>This site was built by <a
href="http://www.ex-parrot.com/~chris/">Chris Lightfoot</a> and <a
href="http://ejhp.net/">Etienne Pollard</a> in two afternoons before
and after Christmas 2005 as a mySociety 'back of the envelope'
project. Chris was a full-time employee of mySociety and spent his
days running much more serious sites like <a
href="http://www.writetothem.com/">WriteToThem.com</a>. <a
href="http://www.mysociety.org/">mySociety</a> is a charitable
organisation which has grown out of the community of volunteers who
built sites like <a
href="http://www.theyworkforyou.com/">TheyWorkForYou.com</a>. Our
primary mission is to build internet projects which give people
simple, tangible benefits in the civic and community aspects of their
lives. Our first project was <a
href="http://www.writetothem.com/">WriteToThem.com</a>, where you can
write to any of your elected representatives, for free, and our more
recent sites include <a
href="http://www.pledgebank.com/">PledgeBank.com</a>.</dd>

EOF

    } elsif ($fn eq 'privacy') {
                hassle_header($q,'Privacy, cookies, and third party services');
                print <<EOF;

                <p><strong>Our use of your data, cookies, and external services: what you should know, and how to opt out if you want to.</strong></p>

                <p>Summary: We care a lot about our users’ privacy. We provide details below, and we try our hardest to look after the private data that we hold. Like many other websites, we sometimes use cookies to help us make our websites better. These tools are very common and used by many other sites, but they do have privacy implications, and as a charity concerned with socially positive uses of the internet, we think it’s important to explain them in full. If you don’t want to share your browsing activities on mySociety’s sites with other companies, you can adjust your usage or install opt-out browser plugins.

                <h3>Measuring website usage (Google Analytics)</h3>

                We use Google Analytics to collect information about how people use this site. We do this to make sure it’s meeting its users’ needs and to understand how we could do it better. Google Analytics stores information such as what pages you visit, how long you are on the site, how you got here, what you click on, and information about your web browser. IP addresses are masked (only a portion is stored) and personal information is only reported in aggregate. We do not allow Google to use or share our analytics data for any purpose besides providing us with analytics information, and we recommend that any user of Google Analytics does the same.

                <p>If you’re unhappy with data about your visit to be used in this way, you can install the <a href="http://tools.google.com/dlpage/gaoptout">official browser plugin for blocking Google Analytics</a>.

                <p>The cookies set by Google Analytics are as follows:

                <table>
                <tr><th scope="col">Name</th><th scope="col">Typical Content</th><th scope="col">Expires</th></tr>
                <tr><td>__utma</td><td>Unique anonymous visitor ID</td><td>2 years</td></tr>
                <tr><td>__utmb</td><td>Unique anonymous session ID</td><td>30 minutes</td></tr>
                <tr><td>__utmz</td><td>Information on how the site was reached (e.g. direct or via a link/search/advertisement)</td><td>6 months</td></tr>
                <tr><td>__utmx</td><td>Which variation of a page you are seeing if we are testing different versions to see which is best</td><td>2 years</td></tr>
                </table>

                <h4>Google’s Official Statement about Analytics Data</h4>

                <p>“This website uses Google Analytics, a web analytics service provided by Google, Inc. (“Google”).  Google Analytics uses “cookies”, which are text files placed on your computer, to help the website analyze how users use the site. The information generated by the cookie about your use of the website (including your IP address) will be transmitted to and stored by Google on servers in the United States . Google will use this information for the purpose of evaluating your use of the website, compiling reports on website activity for website operators and providing other services relating to website activity and internet usage.  Google may also transfer this information to third parties where required to do so by law, or where such third parties process the information on Google’s behalf. Google will not associate your IP address with any other data held by Google.  You may refuse the use of cookies by selecting the appropriate settings on your browser, however please note that if you do this you may not be able to use the full functionality of this website.  By using this website, you consent to the processing of data about you by Google in the manner and for the purposes set out above.”</p>

                <p><a href="http://www.mysociety.org/privacy-online/">More general information on how third party services work</a></p>

                <h3>How to unsubscribe</h3>
                <p>If you’ve been hassled enough, you can click the “Unsubscribe” link at the bottom of any HassleMe email to make sure you won’t be reminded again.</p>

                <h3>Mailing address</h3>
                <p>Our mailing address is: 483 Green Lanes, London, N13 4BS, United Kingdom.</p>

                <h2>Credits</h2>

                <p>Bits of wording taken from the <a href="http://gov.uk/help/cookies">gov.uk cookies page</a> (under the Open Government Licence).</p>
EOF
    } elsif ($fn eq 'terms') {
        fn_terms($q);
    }
    hassle_footer($q);
}

sub fn_terms {
    my $q = shift;
    hassle_header($q);
    my $vars;
    my $token = $q->param('token');
    my $email;

    if (my $checked = check_token($q->param('token'))) {
        if ($checked =~/^TC.(.*)/) {
            ($email) = dbh()->selectrow_array("select email from recipient where id = ?", {}, $1);
            $vars->{token} = $token;
            $vars->{email} = $email;
        }
    }

    if (my $action = $q->param('action')) {
        dbh()->do('insert into tc (email, action) values (?, ?)',
                    {}, $email, $action);
        dbh()->commit();
        $vars->{action} = $action;
    }

    $tt->process('tcs.tt', $vars)
        || die $tt->error;
}
